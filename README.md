# cs75plus-2020-1.5T — 长安 CS75PLUS 2020款（1.5T / 2.0T）车机系统镜像库

本仓库用于**备份 / 镜像存放**长安 CS75PLUS 2020 款车机（**1.5T 与 2.0T 两驱/四驱车型**均适用，同一 **S311-WT** 平台、操作系统 `OS_S311-WT-V8`）的原厂升级包，所有镜像以 **Release 附件**形式提供下载，方便车主自行恢复车机系统。

> ⚠️ 声明：本仓库为非官方镜像备份，与长安汽车及其供应商无关联；固件版权归原厂所有，仅供已购买该车型的车主做个人设备备份/恢复使用，请勿用于商业分发。

---

## 📦 当前版本

| 项目 | 内容 |
|---|---|
| 适用车型 | 长安 **CS75PLUS 2020 款 1.5T / 2.0T**（均为 S311-WT 平台） |
| 平台 | S311-WT（Coagent / 德赛西威 车机），OS 前缀 `OS_S311-WT-V8` |
| OS 版本 | `OS_S311-WT-V8_V00.98.00-191227`（2019-12-27） |
| MCU 版本 | `MC_V8_S311_V0.68C_191220`（2019-12-20） |
| TBOX 版本 | os `0.1.9.23` / bsp `0.4.7.51` / app `5.67s.46`（2019-12-12） |
| 升级包体积 | 约 1.10 GiB（原厂整包） |

> 1.5T 与 2.0T 的区别只在动力总成，**车机主机同属 S311-WT 平台、固件通用**。
> 刷机前请务必在「设置 → 关于 / 系统信息」确认 OS 版本号以 **`OS_S311-WT-V8`** 开头 —— 前缀不符（如 `S401`、`S311-WT-V9`）请勿刷入。

## ⬇️ 下载

本仓库双平台镜像，**国内用户建议走 Gitee**（速度更快）：

| 平台 | 提供的内容 | Release 下载页 |
|---|---|---|
| 🟢 **Gitee（国内推荐）** | OS 系统包 **10 个分卷** + MCU + TBOX(bsp/app) | https://gitee.com/a10463981/cs75plus-2020-1.5T/releases/latest |
| ⚫ GitHub（完整） | 原厂整包 **1.10 GiB 单文件** + 全组件 | https://github.com/a10463981/cs75plus-2020-1.5T/releases/latest |

> ⚠️ **为什么 Gitee 是分卷？** Gitee 免费仓库限制「单个附件 ≤ 100MB、单仓库附件总量 ≤ 1GB」，1.10 GiB 的整包无法整体上传。因此 Gitee 侧把 OS 系统包拆成 10 个 96MB 分卷（合并后与原包**逐字节一致**，MD5 `e4751da5f1f7ec31f85332dce422573b`）；`tbox-os.tar.gz` 与 `wecarspeech.zip` 受配额限制仅 GitHub 提供。

### ① 原厂整包（GitHub，一个文件搞定）

| 文件 | 大小 | MD5 | SHA256 |
|---|---|---|---|
| [`OS_S311-WT-V8_V00.98.00-191227.zip`](https://github.com/a10463981/cs75plus-2020-1.5T/releases/latest) | 1.10 GiB | `659985d992dcfc64705771f8eb093aff` | `187939a54fde57c08ffc58cbb5fc750a2fed59511d874e7ff24ea716f139896f` |

解压后得到完整的 `CoagentUpgrade/` 目录（含 MD5 校验文件与版本说明），**直接把整个 `CoagentUpgrade` 文件夹拷到 U 盘根目录**即可刷机，无需自行拼装。

> 包内附带 `__MACOSX/` 目录是 macOS 打包残留，可忽略/删除，不影响升级。

### ② Gitee 分卷合并（合并后即为 `CoagentUpgrade/Os/update.zip`）

先下载 `update.zip.000` ~ `update.zip.009` 共 10 个文件到**同一目录**，然后合并：

```bash
# Linux / macOS
cat update.zip.000 update.zip.001 update.zip.002 update.zip.003 update.zip.004 \
    update.zip.005 update.zip.006 update.zip.007 update.zip.008 update.zip.009 > update.zip
md5sum update.zip     # 必须是 e4751da5f1f7ec31f85332dce422573b
```

```bat
:: Windows CMD（注意按 000→009 顺序写全）
copy /b update.zip.000+update.zip.001+update.zip.002+update.zip.003+update.zip.004+update.zip.005+update.zip.006+update.zip.007+update.zip.008+update.zip.009 update.zip
certutil -hashfile update.zip MD5
```

```powershell
# Windows PowerShell
$parts = 0..9 | ForEach-Object { "update.zip.{0:D3}" -f $_ }
$out = [IO.File]::Create("$PWD\update.zip")
$parts | ForEach-Object { $in = [IO.File]::OpenRead("$PWD\$_"); $in.CopyTo($out); $in.Close() }
$out.Close()
```

**更省事的办法**：用 7-Zip 右键 `update.zip.000` → `7-Zip` → `提取到当前文件夹`，它会自动按顺序合并并解压出 `update.zip`。

### ③ 包内文件清单（整包已含，无需单独下载）

| 文件 | 组件 | 大小 | MD5 | Gitee 是否有 |
|---|---|---|---|---|
| `CoagentUpgrade/Os/update.zip` | **系统 OS 镜像**（核心） | 956 MB | `e4751da5f1f7ec31f85332dce422573b` | ✅ 分卷 000~009 |
| `CoagentUpgrade/Mcu/McuAppUpdate.img` | MCU 固件 | 470 KB | `6007ec4ddd5d398c10ae9bdb66f9608d` | ✅ |
| `CoagentUpgrade/Tbox/tbox-os.tar.gz` | TBOX 系统 | 95.5 MB | `ead3557546d0811b823dfb496298aca1` | ❌ 额度不足 |
| `CoagentUpgrade/Tbox/tbox-bsp.tar.gz` | TBOX BSP | 5.5 MB | `b05b97dc59c47da16c864d09d7d07060` | ✅ |
| `CoagentUpgrade/Tbox/tbox-app.tar.gz` | TBOX 应用 | 393 KB | `5f5aba5ce584e5a517eac02eaf2b55b0` | ✅ |
| `CoagentUpgrade/SoundData/wecarspeech.zip` | 讯飞语音数据包 | 67 MB | `5d12c4c2541171924f1bcb15d1db20bf` | ❌ 额度不足 |

完整校验表见 [`MD5SUMS.txt`](MD5SUMS.txt)。

### 校验方法

```bash
# Linux / macOS
md5sum update.zip
# 期望：e4751da5f1f7ec31f85332dce422573b
```

```powershell
# Windows PowerShell
Get-FileHash .\update.zip -Algorithm MD5
```

```bat
:: Windows CMD
certutil -hashfile update.zip MD5
```

## 🔧 升级（刷机）说明

升级包必须保持如下目录结构，整体放到 U 盘根目录：

```
U盘根目录/
└── CoagentUpgrade/
    ├── Os/
    │   ├── update.zip          ← 本仓库下载
    │   ├── MD5.txt
    │   └── os_versions.txt
    ├── Mcu/
    │   ├── McuAppUpdate.img    ← 本仓库下载
    │   ├── MD5.txt
    │   └── mcu_versions.txt
    ├── Tbox/
    │   ├── tbox-os.tar.gz      ← 本仓库下载
    │   ├── tbox-bsp.tar.gz
    │   ├── tbox-app.tar.gz
    │   ├── md5.txt
    │   └── tbox_version.txt
    └── SoundData/
        ├── wecarspeech.zip     ← 本仓库下载
        ├── md5.txt
        └── sound_data_versions.txt
```

官方升级流程（原厂包自带校验，`MD5.txt` 与镜像不匹配会拒绝升级）：

1. U 盘格式化为 **FAT32**，把 `CoagentUpgrade` 整个文件夹复制到根目录；
2. 车辆熄火状态插入 U 盘，通电（ACC ON，不要点火）；
3. 车机检测到升级包后自动弹出升级提示 → 确认升级；
4. **升级期间切勿断电、勿拔 U 盘**，全程约 10~20 分钟，完成后自动重启；
5. 升级完成后建议检查：设置 → 关于 → 版本号应变为 `V00.98.00-191227`。

详细步骤与排错见 [`docs/刷机与升级说明.md`](docs/刷机与升级说明.md)。

## 📁 目录结构

```
.
├── README.md                 # 本文件
├── MD5SUMS.txt               # 全部镜像校验值
├── RELEASE_NOTES.md          # GitHub Release 说明
├── RELEASE_NOTES.gitee.md    # Gitee Release 说明（分卷版）
├── docs/
│   ├── 刷机与升级说明.md      # U盘升级 / 工程模式 / 排错
│   └── TBOX-发版记录.md       # TBOX 模块历史发版说明（原厂原文）
└── scripts/
    ├── upload-release.py     # GitHub：一键建库 + 发布 Release
    └── upload-gitee.py       # Gitee：一键建库 + 分卷发布
```

> 镜像文件**不入 git 仓库**（体积过大），统一放在 Release 附件里；仓库仅保存文档与校验表。

## 🗂️ 版本历史

| Release | OS 版本 | 日期 | 说明 |
|---|---|---|---|
| `v1.0.0` | OS_S311-WT-V8_V00.98.00-191227 | 2019-12-27 | 首次镜像归档，含 OS + MCU + TBOX + 语音包全套 |

## ❓ 常见问题

**Q：1.5T 和 2.0T 都能刷吗？**
A：**能。** CS75PLUS 2020 款 1.5T 与 2.0T 使用的是同一套 S311-WT 车机主机（屏幕、主控、MCU 一致），区别仅在动力总成。本仓库固件对两款车型通用。前提：确认你的 OS 版本前缀是 `OS_S311-WT-V8`。

**Q：下载速度慢 / 断线？**
A：GitHub Release 附件服务器在境外，可用 [IDM](https://www.internetdownloadmanager.com/)、`aria2c` 或多线程下载器；国内网络建议直接走上面的 Gitee 镜像。

```bash
aria2c -x 8 -s 8 -k 1M "https://github.com/a10463981/cs75plus-2020-1.5T/releases/download/v1.0.0/OS_S311-WT-V8_V00.98.00-191227.zip"
```

**Q：这包能刷别的车型 / 别的年款吗？**
A：**不可以。** 适用范围仅限 **CS75PLUS 2020 款（1.5T / 2.0T）**。其他年款、其他车系或不同平台（如 `S401`、`S311-WT-V9`）刷入会变砖。刷前务必核对「设置 → 关于」里的 OS 版本前缀。

**Q：刷坏了怎么办？**
A：原厂包可重刷恢复；若完全无法进系统，需进入工程模式（部分版本需专用工具/线缆）或联系 4S 店/原厂服务站。
