#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cs75plus-2020-1.5T 镜像库 —— Gitee 镜像发布脚本（纯标准库）

流程：建仓库 → 推送文档(main) → 创建 Release → 上传附件 → 校验

用法:
    export GITEE_TOKEN=xxxx      # 或写入 scripts/.gitee_token
    python3 scripts/upload-gitee.py --dry-run
    python3 scripts/upload-gitee.py --only 'OS_S311-WT-V8_V00.98.00-191227.zip'
    python3 scripts/upload-gitee.py --probe-mb 150   # 探测附件大小上限

Gitee API: https://gitee.com/api/v5  (token 以 access_token 参数传递)
"""

import argparse
import http.client
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.parse
import uuid
from pathlib import Path

API_HOST = "gitee.com"
API_BASE = "/api/v5"
UA = "cs75plus-mirror-gitee/1.0"
CHUNK = 8 * 1024 * 1024

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

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
TOKEN = ""


def log(m):  print(f"{C_CYN}[{time.strftime('%H:%M:%S')}]{C_RST} {m}", flush=True)
def ok(m):   print(f"{C_GRN}✔{C_RST} {m}", flush=True)
def warn(m): print(f"{C_YLW}⚠{C_RST} {m}", flush=True)
def die(m, c=1):
    print(f"{C_RED}✘ {m}{C_RST}", file=sys.stderr, flush=True)
    sys.exit(c)


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.2f} {u}" if u != "B" else f"{n} B"
        n /= 1024.0


def connect(timeout=120):
    return http.client.HTTPSConnection(API_HOST, timeout=timeout, context=ssl.create_default_context())


def gapi(method, path, params=None, body=None, timeout=90):
    """JSON/form API 调用，返回 (status, obj)。token 以 query 参数附加。"""
    params = dict(params or {})
    params["access_token"] = TOKEN
    url = f"{API_BASE}{path}?" + urllib.parse.urlencode(params)
    conn = connect(timeout)
    try:
        headers = {"User-Agent": UA, "Accept": "application/json"}
        payload = None
        if body is not None:
            payload = urllib.parse.urlencode(body).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        conn.request(method, url, body=payload, headers=headers)
        r = conn.getresponse()
        raw = r.read()
        try:
            obj = json.loads(raw) if raw.strip() else {}
        except Exception:
            obj = {"raw": raw[:400].decode("utf-8", "replace")}
        return r.status, obj
    except Exception as e:
        return 0, {"error": f"{type(e).__name__}: {e}"}
    finally:
        conn.close()


def explain(o):
    if isinstance(o, dict):
        if "message" in o or "error" in o:
            return str(o.get("message") or o.get("error"))[:300]
        return json.dumps(o, ensure_ascii=False)[:300]
    return str(o)[:300]


def upload_attachment(owner, repo, rel_id, path, filename=None, attempts=3):
    """multipart 流式上传 release 附件，返回 (obj|None, err)。"""
    name = filename or Path(path).name
    size = os.path.getsize(path)
    boundary = "----dsh" + uuid.uuid4().hex
    head = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="access_token"\r\n\r\n{TOKEN}\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode()
    tail = f"\r\n--{boundary}--\r\n".encode()
    total = len(head) + size + len(tail)
    path_q = f"{API_BASE}/repos/{owner}/{repo}/releases/{rel_id}/attach_files"

    last = "unknown"
    for attempt in range(1, attempts + 1):
        conn = connect(180)
        t0 = time.time()
        try:
            conn.putrequest("POST", path_q)
            conn.putheader("User-Agent", UA)
            conn.putheader("Accept", "application/json")
            conn.putheader("Content-Type", f"multipart/form-data; boundary={boundary}")
            conn.putheader("Content-Length", str(total))
            conn.endheaders()
            conn.send(head)
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
                        print(f"\r    {name}: {sent*100.0/size:5.1f}%  {human(sent)}/{human(size)}  "
                              f"{human(sent/max(now-t0,.001))}/s   ", end="", flush=True)
                        last_tick = now
            conn.send(tail)
            print("", flush=True)
            r = conn.getresponse()
            raw = r.read()
            try:
                obj = json.loads(raw) if raw.strip() else {}
            except Exception:
                obj = {"raw": raw[:400].decode("utf-8", "replace")}
            if r.status in (200, 201):
                return obj, None
            last = f"HTTP {r.status}: {explain(obj)}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        finally:
            try:
                conn.close()
            except Exception:
                pass
        if attempt < attempts:
            warn(f"{name} 第 {attempt} 次失败（{last}），{8*attempt}s 后重试 ...")
            time.sleep(8 * attempt)
    return None, last


def main():
    global TOKEN
    ap = argparse.ArgumentParser(description="Gitee 镜像发布脚本")
    ap.add_argument("--owner", default="")
    ap.add_argument("--repo", default="cs75plus-2020-1.5T")
    ap.add_argument("--tag", default="v1.0.0")
    ap.add_argument("--title", default="CS75PLUS 2020款 1.5T 车机系统镜像 v1.0.0 (S311-WT)")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--assets", default=str(ROOT / "assets"))
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-push", action="store_true")
    ap.add_argument("--skip-upload", action="store_true")
    ap.add_argument("--probe-mb", type=int, default=0, help="用 N MB 全零文件探测附件大小上限")
    ap.add_argument("--remote", default="gitee", help="git remote 名，默认 gitee（不覆盖 origin）")
    a = ap.parse_args()

    TOKEN = os.environ.get("GITEE_TOKEN", "").strip()
    if not TOKEN:
        for cand in (HERE / ".gitee_token", ROOT / ".gitee_token"):
            if cand.is_file():
                TOKEN = cand.read_text().strip()
                log(f"从 {cand} 读取 token")
                break
    if not TOKEN:
        die("未找到 GITEE_TOKEN")

    st, me = gapi("GET", "/user")
    if st != 200 or "login" not in me:
        die(f"token 无效: HTTP {st} {explain(me)}")
    login = me["login"]
    owner = a.owner or login
    ok(f"已认证(Gitee): {login}")
    log(f"目标: {owner}/{a.repo}  tag={a.tag}")

    # 仓库
    st, body = gapi("GET", f"/repos/{owner}/{a.repo}")
    if st == 200:
        ok(f"仓库已存在: {body.get('html_url')}")
    else:
        log("创建仓库 ...")
        st, body = gapi("POST", "/user/repos", body={
            "name": a.repo,
            "description": "长安 CS75PLUS 2020款 1.5T 车机系统镜像备份库 (S311-WT) — 镜像包通过 Release 下载",
            "private": "false",
            "auto_init": "false",
            "has_issues": "true",
            "has_wiki": "false",
        })
        if st not in (200, 201):
            die(f"创建仓库失败: HTTP {st} {explain(body)}")
        ok(f"仓库已创建: {body.get('html_url')}")

    # 推送文档
    if a.skip_push:
        log("跳过 git 推送")
    else:
        log(f"推送文档到 {a.branch} ...")
        env = dict(os.environ)
        env.update(GIT_AUTHOR_NAME=login, GIT_AUTHOR_EMAIL=f"{login}@users.noreply.gitee.com",
                   GIT_COMMITTER_NAME=login, GIT_COMMITTER_EMAIL=f"{login}@users.noreply.gitee.com")
        # Gitee 支持 https://用户名:token@gitee.com/...
        remote_url = f"https://{owner}:{TOKEN}@gitee.com/{owner}/{a.repo}.git"
        if not (ROOT / ".git").exists():
            subprocess.run(["git", "init", "-q", "-b", a.branch], cwd=ROOT)
        subprocess.run(["git", "remote", "remove", a.remote], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "remote", "add", a.remote, remote_url], cwd=ROOT, check=True)
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "docs: CS75PLUS 2020款 1.5T 车机镜像库说明"],
                       cwd=ROOT, check=False, env=env)
        r = subprocess.run(["git", "push", "-u", a.remote, f"{a.branch}:{a.branch}"],
                           cwd=ROOT, capture_output=True, text=True, env=env)
        subprocess.run(["git", "remote", "set-url", a.remote, f"https://gitee.com/{owner}/{a.repo}.git"], cwd=ROOT)
        if r.returncode != 0:
            die("git 推送失败:\n  " + "\n  ".join((r.stderr or r.stdout).strip().splitlines()[-4:]))
        ok("文档已推送")

    # Release
    st, body = gapi("GET", f"/repos/{owner}/{a.repo}/releases/tags/{a.tag}")
    if st == 200:
        rel = body
        ok(f"Release 已存在 (id={rel['id']})")
    else:
        notes = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
        notes = notes.replace("{{OWNER}}", owner).replace("{{REPO}}", a.repo).replace("{{TAG}}", a.tag)
        notes = notes.replace("github.com", "gitee.com")
        log("创建 Release ...")
        st, body = gapi("POST", f"/repos/{owner}/{a.repo}/releases", body={
            "tag_name": a.tag, "name": a.title, "body": notes,
            "prerelease": "false", "target_commitish": a.branch,
        })
        if st not in (200, 201):
            die(f"创建 Release 失败: HTTP {st} {explain(body)}")
        rel = body
        ok(f"Release 已创建 (id={rel['id']})")

    # 探测大小上限
    if a.probe_mb > 0:
        probe = ROOT / f".probe_{a.probe_mb}mb.bin"
        log(f"生成 {a.probe_mb}MB 探测文件 ...")
        with open(probe, "wb") as fh:
            fh.write(os.urandom(1024) * (a.probe_mb * 1024))
        obj, err = upload_attachment(owner, a.repo, rel["id"], str(probe), filename=f"probe_{a.probe_mb}mb.bin")
        probe.unlink()
        if obj:
            ok(f"{a.probe_mb}MB 上限探测通过 (id={obj.get('id')})")
            st, _ = gapi("DELETE", f"/repos/{owner}/{a.repo}/releases/{rel['id']}/attach_files/{obj.get('id')}")
            log(f"已删除探测附件 HTTP {st}")
        else:
            warn(f"{a.probe_mb}MB 探测失败: {err}")
        return 0

    if a.skip_upload:
        log("跳过附件上传")
        return 0

    # 附件
    assets_dir = Path(a.assets)
    files = [p for p in assets_dir.iterdir() if p.is_file() and not p.name.startswith(".")]
    if a.only:
        wanted = {x.strip() for x in a.only.split(",") if x.strip()}
        files = [p for p in files if p.name in wanted]
    rank = {n: i for i, n in enumerate(PREFERRED_ORDER)}
    files.sort(key=lambda p: (rank.get(p.name, len(rank)), -p.stat().st_size))

    st, existing = gapi("GET", f"/repos/{owner}/{a.repo}/releases/{rel['id']}/attach_files", {"per_page": 100})
    have = {x["name"]: x for x in (existing if isinstance(existing, list) else [])}

    failed = []
    for f in files:
        size = os.path.getsize(f)
        old = have.get(f.name)
        if old and old.get("size") == size:
            ok(f"已存在且大小一致，跳过: {f.name}")
            continue
        if old:
            warn(f"{f.name} 大小不符（远端 {old.get('size')}），删除后重传")
            gapi("DELETE", f"/repos/{owner}/{a.repo}/releases/{rel['id']}/attach_files/{old['id']}")
        log(f"上传 {f.name} ({human(size)}) ...")
        obj, err = upload_attachment(owner, a.repo, rel["id"], str(f))
        if not obj:
            failed.append((f.name, err))
            warn(f"上传失败: {f.name} -> {err}")
            continue
        ok(f"完成: {f.name}  url={obj.get('browser_download_url') or obj.get('download_url') or '-'}")

    st, final = gapi("GET", f"/repos/{owner}/{a.repo}/releases/{rel['id']}/attach_files", {"per_page": 100})
    final = final if isinstance(final, list) else []
    log("远端附件:")
    for x in final:
        print(f"    {human(x.get('size', 0)):>10}  {x['name']}  {x.get('browser_download_url', '')}")
    print()
    print(f"  📄 Gitee 仓库: https://gitee.com/{owner}/{a.repo}")
    print(f"  🏷️  发布页:   https://gitee.com/{owner}/{a.repo}/releases/tag/{a.tag}")
    print()
    if failed:
        die(f"{len(failed)} 个附件未完成")
    ok("Gitee 全部完成")


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except KeyboardInterrupt:
        die("已中断", 130)
