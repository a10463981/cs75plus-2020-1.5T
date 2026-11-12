#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 CS75PLUS 2020 车机镜像在 Gitee 批量创建「单版本专用仓库」并发布 Release。
用法: python3 scripts/publish-gitee-mirrors.py [--only 191016,200512,201025]
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
import uuid
from pathlib import Path

API_HOST = "gitee.com"
API_BASE = "/api/v5"
UA = "cs75plus-gitee-mirror/1.0"
CHUNK = 8 * 1024 * 1024
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = Path(os.environ.get("MIRROR_SRC", "/vol1/@appshare/fn-deepseek-harness/车载APK/gitee_repos"))

C_RED, C_GRN, C_YLW, C_CYN, C_RST = "\033[31m", "\033[32m", "\033[33m", "\033[36m", "\033[0m"
TOKEN = ""

REPOS = [
    dict(key="191016", repo="cs75plus-2020-1.5T-191016", tag="v0.75.00-191016",
         title="CS75PLUS 2020款（1.5T / 2.0T）车机系统 V00.75.00-191016 (S311-WT)",
         desc="CS75PLUS 2020款 1.5T/2.0T 车机镜像 V00.75.00-191016（最旧版本）— S311-WT 平台"),
    dict(key="200512", repo="cs75plus-2020-1.5T-200512", tag="v1.09.00-200512",
         title="CS75PLUS 2020款（1.5T / 2.0T）车机系统 V01.09.00-200512 双导航版 (S311-WT)",
         desc="CS75PLUS 2020款 1.5T/2.0T 车机镜像 V01.09.00-200512（双导航版）— S311-WT 平台"),
    dict(key="netfix", repo="cs75plus-2020-1.5T-netfix", tag="tbox-netfix-191227",
         title="CS75PLUS 2020款（1.5T / 2.0T）4G 网络修复包（TBOX 重刷，来自 V00.98.00-191227）",
         desc="CS75PLUS 2020款 1.5T/2.0T 车机 4G 网络修复包（TBOX 重刷）— S311-WT 平台"),
    dict(key="201025", repo="cs75plus-2020-1.5T-201025", tag="v1.25.11-201025",
         title="CS75PLUS 2020款（1.5T / 2.0T）车机系统 V1.25.11-201025 最新版 (S311-WT)",
         desc="CS75PLUS 2020款 1.5T/2.0T 车机镜像 V1.25.11-201025（最新版，完整原厂 RAR）— S311-WT 平台"),
]


def log(m):  print(f"{C_CYN}[{time.strftime('%H:%M:%S')}]{C_RST} {m}", flush=True)
def ok(m):   print(f"{C_GRN}✔{C_RST} {m}", flush=True)
def warn(m): print(f"{C_YLW}⚠{C_RST} {m}", flush=True)
def die(m, c=1):
    print(f"{C_RED}✘ {m}{C_RST}", file=sys.stderr, flush=True)
    sys.exit(c)


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.1f} {u}" if u != "B" else f"{n} B"
        n /= 1024.0


def connect(timeout=120):
    return http.client.HTTPSConnection(API_HOST, timeout=timeout, context=ssl.create_default_context())


def gapi(method, path, params=None, body=None, timeout=90):
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
            obj = {"raw": raw[:300].decode("utf-8", "replace")}
        return r.status, obj
    except Exception as e:
        return 0, {"error": f"{type(e).__name__}: {e}"}
    finally:
        conn.close()


def explain(o):
    if isinstance(o, dict):
        return str(o.get("message") or o.get("error") or json.dumps(o, ensure_ascii=False)[:200])
    return str(o)[:200]


def upload_attachment(owner, repo, rel_id, path, filename=None, attempts=4):
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
            tick = 0.0
            with open(path, "rb") as fh:
                while True:
                    c = fh.read(CHUNK)
                    if not c:
                        break
                    conn.send(c)
                    sent += len(c)
                    now = time.time()
                    if now - tick >= 10 or sent == size:
                        print(f"\r    {name}: {sent*100.0/size:5.1f}%  {human(sent)}/{human(size)}  "
                              f"{human(sent/max(now-t0,.001))}/s   ", end="", flush=True)
                        tick = now
            conn.send(tail)
            print("", flush=True)
            r = conn.getresponse()
            raw = r.read()
            try:
                obj = json.loads(raw) if raw.strip() else {}
            except Exception:
                obj = {"raw": raw[:300].decode("utf-8", "replace")}
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


def ensure_repo(owner, name, desc):
    st, body = gapi("GET", f"/repos/{owner}/{name}")
    if st == 200:
        ok(f"仓库已存在: {name}")
    else:
        log(f"创建仓库 {name} ...")
        st, body = gapi("POST", "/user/repos", body={
            "name": name, "description": desc,
            "auto_init": "false", "has_issues": "true", "has_wiki": "false",
        })
        if st not in (200, 201):
            die(f"创建 {name} 失败: HTTP {st} {explain(body)}")
        ok(f"仓库已创建: {body.get('html_url')}")


def make_public(owner, name):
    """Gitee 空仓库不允许设为公开，必须推送内容后再改。"""
    st, cur = gapi("GET", f"/repos/{owner}/{name}")
    if not isinstance(cur, dict):
        warn(f"查询仓库状态失败: {explain(cur)}")
        return False
    if not cur.get("private"):
        ok("仓库可见性: 公开")
        return True
    warn("仓库当前为私有，改为公开 ...")
    st2, b2 = gapi("PATCH", f"/repos/{owner}/{name}", body={"name": name, "private": "false"})
    if st2 != 200:
        warn(f"改公开失败: {explain(b2)}")
        return False
    ok("已设为公开")
    return True


def push_readme(owner, name, repo_dir, branch="main"):
    env = dict(os.environ)
    env.update(GIT_AUTHOR_NAME=owner, GIT_AUTHOR_EMAIL=f"{owner}@users.noreply.gitee.com",
               GIT_COMMITTER_NAME=owner, GIT_COMMITTER_EMAIL=f"{owner}@users.noreply.gitee.com")
    subprocess.run(["git", "init", "-q", "-b", branch], cwd=repo_dir, check=False)
    subprocess.run(["git", "add", "-A"], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "docs: 初始化单版本镜像仓说明"], cwd=repo_dir, check=False, env=env)
    url = f"https://{owner}:{TOKEN}@gitee.com/{owner}/{name}.git"
    subprocess.run(["git", "remote", "remove", "origin"], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", url], cwd=repo_dir, check=True)
    r = subprocess.run(["git", "push", "-q", "-u", "origin", f"{branch}:{branch}"],
                       cwd=repo_dir, capture_output=True, text=True, env=env)
    subprocess.run(["git", "remote", "set-url", "origin", f"https://gitee.com/{owner}/{name}.git"], cwd=repo_dir)
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip().splitlines()[-3:]
    return True, None


def main():
    global TOKEN
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default="a10463981")
    ap.add_argument("--only", default="")
    ap.add_argument("--skip-upload", action="store_true")
    a = ap.parse_args()

    TOKEN = os.environ.get("GITEE_TOKEN", "").strip()
    if not TOKEN:
        f = HERE / ".gitee_token"
        if f.is_file():
            TOKEN = f.read_text().strip()
    if not TOKEN:
        die("未找到 GITEE_TOKEN")

    st, me = gapi("GET", "/user")
    if st != 200:
        die(f"token 无效: HTTP {st}")
    ok(f"已认证(Gitee): {me['login']}")
    owner = a.owner or me["login"]

    want = {x.strip() for x in a.only.split(",") if x.strip()}
    results = []
    for cfg in REPOS:
        if want and cfg["key"] not in want:
            continue
        key, name, tag = cfg["key"], cfg["repo"], cfg["tag"]
        assets = SRC / key / "assets"
        repo_dir = SRC / key / "repo"
        files = [p for p in assets.iterdir() if p.is_file()]
        # 分卷在前（按名排序保证顺序），小件在后
        files.sort(key=lambda p: (0 if ".0" in p.name else 1, p.name))
        total = sum(os.path.getsize(p) for p in files)
        if total >= 1073741824:
            die(f"{name} 资产合计 {total} B 超过 1 GiB，中止")
        log(f"===== {name} ===== {len(files)} 个文件 / {human(total)}")

        ensure_repo(owner, name, cfg["desc"])

        okk, err = push_readme(owner, name, repo_dir)
        if okk:
            ok("README 已推送")
        else:
            warn("README 推送失败：" + " | ".join(err or []))
        make_public(owner, name)

        st, rel = gapi("GET", f"/repos/{owner}/{name}/releases/tags/{tag}")
        if st == 200 and isinstance(rel, dict) and rel.get("id"):
            ok(f"Release 已存在 (id={rel['id']})")
        else:
            notes = f"""## {cfg['title']}

长安 CS75PLUS 2020 款（1.5T / 2.0T）车机原厂升级包镜像，平台 **S311-WT / OS_S311-WT-V8**。

> 本仓库是 [主库 cs75plus-2020-1.5T](https://gitee.com/a10463981/cs75plus-2020-1.5T) 的单版本专用镜像仓。
> Gitee 免费仓库限制「单附件 ≤ 100MB、单仓库附件总量 ≤ 1GB」，因此按版本分仓，并把大镜像拆成分卷。

### 📦 本页附件

共 {len(files)} 个文件、合计 {human(total)}：

- `{cfg['key']}` 版本镜像分卷（每个 96 MB）
- 配套的小组件文件（MCU / TBOX / 说明书等）

**分卷合并**：下载全部卷到同一目录后

```bash
cat <文件名>.0* > <目标文件>
```
或 Windows：`copy /b 第1卷+第2卷+...+末卷 目标文件`；也可用 7-Zip 右键 `.000` → 提取。

完整说明与校验值见 [README](https://gitee.com/a10463981/{name}#)
及主库 [版本清单](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/版本清单.md)。

> ⚠️ 仅适用于 CS75PLUS 2020 款 1.5T / 2.0T（S311-WT 平台）。非官方备份，固件版权归原厂所有。
"""
            st, rel = gapi("POST", f"/repos/{owner}/{name}/releases", body={
                "tag_name": tag, "name": cfg["title"], "body": notes,
                "prerelease": "false", "target_commitish": "main",
            })
            if st not in (200, 201):
                warn(f"创建 Release 失败: HTTP {st} {explain(rel)}")
                results.append((name, "release-failed"))
                continue
            ok(f"Release 已创建 (id={rel['id']})")

        if a.skip_upload:
            continue

        st, existing = gapi("GET", f"/repos/{owner}/{name}/releases/{rel['id']}/attach_files", {"per_page": 100})
        have = {x["name"]: x for x in (existing if isinstance(existing, list) else [])}
        failed = []
        for f in files:
            size = os.path.getsize(f)
            old = have.get(f.name)
            if old and old.get("size") == size:
                ok(f"已存在，跳过: {f.name}")
                continue
            if old:
                gapi("DELETE", f"/repos/{owner}/{name}/releases/{rel['id']}/attach_files/{old['id']}")
            log(f"上传 {f.name} ({human(size)}) ...")
            obj, err = upload_attachment(owner, name, rel["id"], str(f))
            if not obj:
                failed.append(f.name)
                warn(f"失败: {f.name} -> {err}")
                continue
            ok(f"完成: {f.name} ({human(obj.get('size') or 0)})")

        st, final = gapi("GET", f"/repos/{owner}/{name}/releases/{rel['id']}/attach_files", {"per_page": 100})
        final = final if isinstance(final, list) else []
        got = sum(x.get("size") or 0 for x in final)
        ok(f"{name}: {len(final)} 个附件 / {got} B（目标 {total} B）")
        results.append((name, "ok" if not failed and got == total else f"{len(failed)} 个失败"))

    print()
    for n, s in results:
        print(f"  {n}: {s}")
    if any(s != "ok" for _, s in results):
        die("有仓库未完成，可重跑本脚本（已上传会跳过）")
    ok("全部完成")


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except KeyboardInterrupt:
        die("已中断", 130)
