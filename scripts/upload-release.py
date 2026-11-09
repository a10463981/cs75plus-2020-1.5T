#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cs75plus-2020-1.5T 镜像库维护脚本（无第三方依赖，仅标准库）

一键完成：建 Public 仓库 → 推送文档 → 创建 Release → 流式上传镜像附件 → 校验。

用法:
    export GITHUB_TOKEN=ghp_xxx        # 或写入 scripts/.token
    python3 scripts/upload-release.py --dry-run      # 只检查本地文件
    python3 scripts/upload-release.py                # 正式执行
    python3 scripts/upload-release.py --tag v1.0.1 --assets ./assets2

Token 权限: classic PAT 勾选 repo; fine-grained 需 Administration: RW + Contents: RW。
"""

import argparse
import http.client
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
UPLOAD_HOST = "uploads.github.com"
UA = "cs75plus-mirror-tool/1.0"
CHUNK = 8 * 1024 * 1024

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# 优先上传顺序：原厂整包最优先，其后按体积降序（尽早暴露大文件网络问题）
PREFERRED_ORDER = [
    "OS_S311-WT-V8_V00.98.00-191227.zip",
    "update.zip",
    "tbox-os.tar.gz",
    "wecarspeech.zip",
    "tbox-bsp.tar.gz",
    "tbox-app.tar.gz",
    "McuAppUpdate.img",
]

C_RED, C_GRN, C_YLW, C_CYN, C_RST = "\033[31m", "\033[32m", "\033[33m", "\033[36m", "\033[0m"


def log(msg):
    print(f"{C_CYN}[{time.strftime('%H:%M:%S')}]{C_RST} {msg}", flush=True)


def ok(msg):
    print(f"{C_GRN}✔{C_RST} {msg}", flush=True)


def warn(msg):
    print(f"{C_YLW}⚠{C_RST} {msg}", flush=True)


def die(msg, code=1):
    print(f"{C_RED}✘ {msg}{C_RST}", file=sys.stderr, flush=True)
    sys.exit(code)


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.2f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0


# --------------------------------------------------------------------- HTTP
TOKEN = ""


def api(method, path, payload=None, timeout=60):
    """调用 GitHub REST API，返回 (status, dict)。"""
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", UA)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            body = json.loads(raw) if raw.strip() else {}
        except Exception:
            body = {"raw": raw[:400].decode("utf-8", "replace")}
        return e.code, body
    except Exception as e:  # 网络层错误
        return 0, {"error": f"{type(e).__name__}: {e}"}


def explain(body):
    if not isinstance(body, dict):
        return str(body)[:300]
    if "message" in body:
        extra = body.get("errors")
        return f"{body['message']}" + (f" | {json.dumps(extra, ensure_ascii=False)[:300]}" if extra else "")
    return str(body)[:300]


# ------------------------------------------------------------------ upload
def upload_asset(owner, repo, rel_id, name, path, attempts=4):
    """流式上传单个 release 资产，返回 (asset_dict | None, err)"""
    size = os.path.getsize(path)
    url_path = f"/repos/{owner}/{repo}/releases/{rel_id}/assets?name={urllib.parse.quote(name)}"
    last_err = "unknown"

    for attempt in range(1, attempts + 1):
        t0 = time.time()
        conn = None
        try:
            conn = http.client.HTTPSConnection(
                UPLOAD_HOST, timeout=120, context=ssl.create_default_context()
            )
            conn.putrequest("POST", url_path)
            conn.putheader("Authorization", f"Bearer {TOKEN}")
            conn.putheader("Accept", "application/vnd.github+json")
            conn.putheader("X-GitHub-Api-Version", "2022-11-28")
            conn.putheader("User-Agent", UA)
            conn.putheader("Content-Type", "application/octet-stream")
            conn.putheader("Content-Length", str(size))
            conn.endheaders()

            sent = 0
            last_tick = 0.0
            with open(path, "rb") as fh:
                while True:
                    chunk = fh.read(CHUNK)
                    if not chunk:
                        break
                    conn.send(chunk)
                    sent += len(chunk)
                    now = time.time()
                    if now - last_tick >= 5 or sent == size:
                        pct = sent * 100.0 / size if size else 100
                        rate = sent / max(now - t0, 0.001)
                        print(
                            f"\r    {name}: {pct:5.1f}%  {human(sent)}/{human(size)}  "
                            f"{human(rate)}/s   ",
                            end="",
                            flush=True,
                        )
                        last_tick = now
            print("", flush=True)

            resp = conn.getresponse()
            raw = resp.read()
            status = resp.status
            try:
                body = json.loads(raw) if raw.strip() else {}
            except Exception:
                body = {"raw": raw[:400].decode("utf-8", "replace")}

            if status in (200, 201) and isinstance(body, dict) and body.get("size") == size:
                return body, None
            if status in (200, 201):
                return body, f"远端大小 {body.get('size')} != 本地 {size}"
            last_err = f"HTTP {status}: {explain(body)}"
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

        if attempt < attempts:
            wait = 10 * attempt
            warn(f"{name} 第 {attempt} 次失败（{last_err}），{wait}s 后重试 ...")
            time.sleep(wait)

    return None, last_err


# -------------------------------------------------------------------- main
def main():
    global TOKEN
    p = argparse.ArgumentParser(description="CS75PLUS 2020 1.5T 车机镜像库发布脚本")
    p.add_argument("--owner", default="", help="仓库所属用户（默认取 token 对应账号）")
    p.add_argument("--repo", default="cs75plus-2020-1.5T")
    p.add_argument("--tag", default="v1.0.0")
    p.add_argument("--title", default="CS75PLUS 2020款 1.5T 车机系统镜像 v1.0.0 (S311-WT)")
    p.add_argument("--branch", default="main")
    p.add_argument("--assets", default=str(ROOT / "assets"))
    p.add_argument("--only", default="", help="只上传指定文件名（逗号分隔），默认上传 assets/ 内全部")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-push", action="store_true")
    a = p.parse_args()

    assets_dir = Path(a.assets)
    log(f"资产目录: {assets_dir}")
    if not assets_dir.is_dir():
        die(f"资产目录不存在: {assets_dir}")

    # 本地资产清单：自动发现目录内所有文件（软链指向的真实文件）
    for p in sorted(assets_dir.iterdir()):
        if p.is_symlink() and not p.exists():
            warn(f"断链，忽略: {p.name} -> {os.readlink(p)}")

    files = [p for p in assets_dir.iterdir() if p.is_file() and not p.name.startswith(".")]
    if a.only:
        wanted = {x.strip() for x in a.only.split(",") if x.strip()}
        files = [p for p in files if p.name in wanted]
        for n in sorted(wanted - {p.name for p in files}):
            warn(f"--only 指定的文件不存在: {n}")
    rank = {n: i for i, n in enumerate(PREFERRED_ORDER)}
    files.sort(key=lambda p: (rank.get(p.name, len(rank)), -p.stat().st_size))

    present = [(p.name, p) for p in files]
    total = sum(os.path.getsize(f) for _, f in present)
    for n, f in present:
        ok(f"{n:<42} {human(os.path.getsize(f)):>10}")
    log(f"待上传 {len(present)} 个文件，合计 {human(total)}")

    if a.dry_run:
        log("DRY RUN 结束（未访问 GitHub）")
        return 0
    if not present:
        die("没有可上传的文件")

    # token
    TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
    if not TOKEN:
        for cand in (HERE / ".token", ROOT / ".token", Path.home() / ".github_token"):
            if cand.is_file():
                TOKEN = cand.read_text().strip()
                log(f"从 {cand} 读取 token")
                break
    if not TOKEN:
        die("未找到 GITHUB_TOKEN（环境变量或 scripts/.token）")

    # 身份
    st, me = api("GET", "/user")
    if st != 200 or "login" not in me:
        die(f"token 无效或权限不足: HTTP {st} {explain(me)}")
    login = me["login"]
    owner = a.owner or login
    ok(f"已认证: {login}" + ("" if owner == login else f"（仓库将建在 {owner} 名下）"))
    log(f"目标: {owner}/{a.repo}  tag={a.tag}  branch={a.branch}")

    # 1. 仓库
    st, body = api("GET", f"/repos/{owner}/{a.repo}")
    if st == 200:
        ok(f"仓库已存在: {body.get('html_url')}")
    else:
        log("创建仓库 ...")
        st, body = api(
            "POST",
            "/user/repos",
            {
                "name": a.repo,
                "description": "长安 CS75PLUS 2020款 1.5T 车机系统镜像备份库 (S311-WT) — 镜像包通过 Release 下载",
                "private": False,
                "has_issues": True,
                "has_wiki": False,
                "has_projects": False,
                "auto_init": False,
            },
        )
        if st != 201:
            die(f"创建仓库失败: HTTP {st} {explain(body)}")
        ok(f"仓库已创建: {body.get('html_url')}")

    # 2. 推送文档（Release 需要至少一个 commit 作为 tag 目标）
    if a.skip_push:
        log("跳过 git 推送 (--skip-push)")
    else:
        log(f"推送文档到 {a.branch} ...")
        env = dict(os.environ)
        env.update(
            GIT_AUTHOR_NAME=login,
            GIT_AUTHOR_EMAIL=f"{login}@users.noreply.github.com",
            GIT_COMMITTER_NAME=login,
            GIT_COMMITTER_EMAIL=f"{login}@users.noreply.github.com",
        )
        remote = f"https://x-access-token:{TOKEN}@github.com/{owner}/{a.repo}.git"
        cmds = [
            ["git", "init", "-q", "-b", a.branch],
        ]
        if not (ROOT / ".git").exists():
            for c in cmds:
                subprocess.run(c, cwd=ROOT, check=False)
        subprocess.run(["git", "remote", "remove", "origin"], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", remote], cwd=ROOT, check=True)
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "docs: CS75PLUS 2020款 1.5T 车机镜像库说明"], cwd=ROOT, check=False, env=env)
        r = subprocess.run(["git", "push", "-u", "origin", a.branch], cwd=ROOT, capture_output=True, text=True, env=env)
        subprocess.run(["git", "remote", "set-url", "origin", f"https://github.com/{owner}/{a.repo}.git"], cwd=ROOT)
        if r.returncode != 0:
            tail = (r.stderr or r.stdout or "").strip().splitlines()[-4:]
            die("git 推送失败，Release 需要 commit 作为 tag 目标，已中止:\n  " + "\n  ".join(tail))
        ok("文档已推送")

    # 3. Release
    st, body = api("GET", f"/repos/{owner}/{a.repo}/releases/tags/{a.tag}")
    if st == 200:
        rel = body
        ok(f"Release 已存在 (id={rel['id']})")
    else:
        notes = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
        notes = notes.replace("{{OWNER}}", owner).replace("{{REPO}}", a.repo).replace("{{TAG}}", a.tag)
        log("创建 Release ...")
        st, body = api(
            "POST",
            f"/repos/{owner}/{a.repo}/releases",
            {
                "tag_name": a.tag,
                "name": a.title,
                "body": notes,
                "draft": False,
                "prerelease": False,
                "make_latest": "true",
                "target_commitish": a.branch,
            },
        )
        if st != 201:
            die(f"创建 Release 失败: HTTP {st} {explain(body)}")
        rel = body
        ok(f"Release 已创建 (id={rel['id']}): {rel.get('html_url')}")

    # 4. 上传
    st, existing = api("GET", f"/repos/{owner}/{a.repo}/releases/{rel['id']}/assets?per_page=100")
    existing = {x["name"]: x for x in (existing if isinstance(existing, list) else [])}

    failed = []
    for name, f in present:
        size = os.path.getsize(f)
        old = existing.get(name)
        if old and old.get("size") == size:
            ok(f"已存在且大小一致，跳过: {name} ({human(size)})")
            continue
        if old:
            warn(f"{name} 已存在但大小不符（远端 {old.get('size')}），删除后重传")
            s2, _ = api("DELETE", f"/repos/{owner}/{a.repo}/releases/assets/{old['id']}")
            log(f"删除旧资产 HTTP {s2}")

        log(f"上传 {name} ({human(size)}) ...")
        asset, err = upload_asset(owner, a.repo, rel["id"], name, f)
        if asset is None:
            failed.append((name, err))
            warn(f"上传失败: {name} -> {err}")
            continue
        digest = asset.get("digest")
        ok(f"完成: {name} ({human(asset['size'])}) {('digest=' + digest) if digest else ''}")
        ok(f"    {asset.get('browser_download_url')}")

    # 5. 汇总
    log("汇总远端资产 ...")
    st, final = api("GET", f"/repos/{owner}/{a.repo}/releases/{rel['id']}/assets?per_page=100")
    final = final if isinstance(final, list) else []
    remote_total = 0
    for x in sorted(final, key=lambda i: i["name"]):
        remote_total += x["size"]
        print(f"    {x['state']:<12} {human(x['size']):>10}  {x['name']}  {x.get('digest') or ''}")
    ok(f"远端合计 {human(remote_total)} / 本地 {human(total)}")

    print()
    print(f"  📄 仓库: https://github.com/{owner}/{a.repo}")
    print(f"  🏷️  发布: https://github.com/{owner}/{a.repo}/releases/tag/{a.tag}")
    print(f"  ⬇️  最新: https://github.com/{owner}/{a.repo}/releases/latest")
    print()
    if failed:
        die(f"{len(failed)} 个文件未完成，可重跑本脚本（已上传的会自动跳过）")
    if remote_total != total:
        die(f"远端总量与本地不一致（{remote_total} vs {total}）")
    ok("全部完成 ✔")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        die("\n已中断", 130)
