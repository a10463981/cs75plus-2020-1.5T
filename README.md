# cs75plus-2020-1.5T — 长安 CS75PLUS 2020款（1.5T / 2.0T）车机系统镜像库

本仓库用于**备份 / 镜像存放**长安 CS75PLUS 2020 款车机（**1.5T 与 2.0T 两驱/四驱车型**均适用，同一 **S311-WT** 平台、操作系统 `OS_S311-WT-V8`）的原厂升级包，所有镜像以 **Release 附件**形式提供下载，方便车主自行恢复车机系统。

> ⚠️ 声明：本仓库为非官方镜像备份，与长安汽车及其供应商无关联；固件版权归原厂所有，仅供已购买该车型的车主做个人设备备份/恢复使用，请勿用于商业分发。

---

## 📦 已收录版本（4 个，全部实测核验）

| # | 版本 | OS 系统版本 | MCU | 组件 | 类型 | Release |
|---|---|---|---|---|---|---|
| 4 | **`201025`（最新）** | `V1.25.11-201025` | `V0.71C_200812` | OS+MCU | 完整系统+MCU（精简） | [v1.25.11-201025](https://github.com/a10463981/cs75plus-2020-1.5T/releases/tag/v1.25.11-201025) |
| 3 | `200512` | `V01.09.00-200512` | `V0.70C_200421` | OS+MCU+TBOX | 完整包 · **双导航版** | [v1.09.00-200512](https://github.com/a10463981/cs75plus-2020-1.5T/releases/tag/v1.09.00-200512) |
| 2 | `191227` | `V00.98.00-191227` | `V0.68C_191220` | OS+MCU+TBOX+语音 | 完整包（组件最全） | [v0.98.00-191227](https://github.com/a10463981/cs75plus-2020-1.5T/releases/tag/v0.98.00-191227) |
| 1 | `191016` | `V00.75.00-191016` | `V0.58C_191014C` | OS+MCU+TBOX+语音 | 完整包（最旧） | [v0.75.00-191016](https://github.com/a10463981/cs75plus-2020-1.5T/releases/tag/v0.75.00-191016) |

| 项目 | 内容 |
|---|---|
| 适用车型 | 长安 **CS75PLUS 2020 款 1.5T / 2.0T**（均为 S311-WT 平台） |
| 平台 | S311-WT（Coagent / 德赛西威 车机），OS 前缀 `OS_S311-WT-V8` |
| 包的性质 | **4 个都是完整包，没有补丁/增量包**（每个都含完整 OS 镜像） |

### 🧩 各版本 TBOX（4G 通信模块）版本对照

| 版本 | TBOX buildTime | TBOX OS | TBOX BSP | TBOX APP | 本包是否含 TBOX | 本版 TBOX 发版记录 |
|---|---|---|---|---|---|---|
| `191016` | 20191016 | 0.1.9.23 | 0.4.5.49 | 5.62s.42 | ✅ | [记录（28 章节）](docs/TBOX-发版记录-191016.md) |
| `191227` | 20191212 | 0.1.9.23 | 0.4.7.51 | 5.67s.46 | ✅ | [记录（34 章节）](docs/TBOX-发版记录-191227.md) |
| `200512` | 20200402 | 0.1.9.23 | 0.4.8.52 | 5.67s.46 | ✅ | [记录（原厂未更新）](docs/TBOX-发版记录-200512.md) |
| `201025` | — | — | — | — | ❌ 仅 OS+MCU，不更新 TBOX | —（无 TBOX 组件） |

> **每个版本的 TBOX 发版记录独立存放**，不互相覆盖，便于比对「这一版修了什么、还缺什么」；各版修复差异与演进时间线见 [`docs/TBOX-发版记录.md`](docs/TBOX-发版记录.md)（索引页）。
> ⚠️ `200512` 版的 TBOX 三件套实际已替换（BSP `0.4.7.51` → `0.4.8.52`，MD5 全变），但**原厂未更新发版记录**（文件与 `191227` 字节完全相同），`0.4.8.52` 修了什么无文档可查。

> 🔍 逐包分析（补丁/完整、新旧、组件差异、校验值）见 **[`docs/版本清单.md`](docs/版本清单.md)**。

> 1.5T 与 2.0T 的区别只在动力总成，**车机主机同属 S311-WT 平台、固件通用**。
> 刷机前请务必在「设置 → 关于 / 系统信息」确认 OS 版本号以 **`OS_S311-WT-V8`** 开头 —— 前缀不符（如 `S401`、`S311-WT-V9`）请勿刷入。

## 🔧 4G 网络故障修复包（TBOX 重刷）

车机 **4G 模块无法联网**时的专用修复包，**只重刷 TBOX，不动 OS / MCU / 语音**。

| 项目 | 内容 |
|---|---|
| 文件 | `CoagentUpgrade.zip`（101.3 MiB，内部只有 `CoagentUpgrade/Tbox/`） |
| 校验 | MD5 `a32b7e9c1bfb6e415b341de2aed1d243` · SHA256 `3f4528fe…10 85` |
| 下载 | [GitHub 单文件](https://github.com/a10463981/cs75plus-2020-1.5T/releases/tag/tbox-netfix-191227) · [Gitee 分 2 卷](https://gitee.com/a10463981/cs75plus-2020-1.5T-netfix) |
| 成分 | 与 `v0.98.00-191227` 的 TBOX **逐字节完全一致**（7 个文件 MD5 全同），不含新代码 |

**判定逻辑（关键）**：刷入后恢复 → 属软件/证书类故障；**刷入后仍无网络 → 软件层已排除，基本可 100% 判定硬件故障**（4G 模块烧毁或保险丝熔断）。

**能修**：证书异常、`server.conf`/APN 配置写坏、升级中断遗留、远程控制失效。
**修不了**：模块本体烧毁、供电电路/保险丝、天线线束、SIM 欠费、运营商覆盖。

**硬件故障两条路**：① 整车断电 5~10 分钟（拆电瓶，假死可恢复，0 元）；② 拆车机送修（网修约 **100 元**，4S 只换不修约 **2000 元**）。

> 📖 完整拆解、判定流程图与真实故障复盘（电瓶亏电→搭电→4G 失效）见 **[`docs/4G网络故障-修复包与判定.md`](docs/4G网络故障-修复包与判定.md)**。

## ⬇️ 下载

本仓库双平台镜像，**国内用户建议走 Gitee**（速度更快）：

| 平台 | 提供的内容 | 入口 |
|---|---|---|
| 🟢 **Gitee（国内加速）** | **4 个版本分仓**（主库 + 3 个版本专用仓库），详见下表 | https://gitee.com/a10463981/cs75plus-2020-1.5T/releases/latest |
| ⚫ **GitHub（全量）** | 全部 4 个版本，每个都是**完整原厂归档**（含语音包 / `tbox-os` 等超配额文件） | https://github.com/a10463981/cs75plus-2020-1.5T/releases |

### 🗂️ Gitee 分仓索引

Gitee 免费仓库硬限制「**单个附件 ≤ 100MB、单仓库附件总量 ≤ 1GB**」（[官方说明](https://help.gitee.com/repository/release/create)），
单个版本的原厂归档普遍超过 1 GiB，**放不进同一个仓库** —— 因此按版本分仓，每个仓库各自用满 1 GiB 额度：

| 版本 | Gitee 仓库 | 本仓内容 | 配额占用 |
|---|---|---|---|
| `v0.98.00-191227` | [cs75plus-2020-1.5T](https://gitee.com/a10463981/cs75plus-2020-1.5T)（主库） | OS 10 分卷 + MCU + TBOX bsp/app | 962 MiB（94%） |
| `v0.75.00-191016` | [cs75plus-2020-1.5T-191016](https://gitee.com/a10463981/cs75plus-2020-1.5T-191016) | OS 10 分卷 + MCU + TBOX os/bsp/app | 976 MiB（95%） |
| `v1.09.00-200512` | [cs75plus-2020-1.5T-200512](https://gitee.com/a10463981/cs75plus-2020-1.5T-200512) | OS 11 分卷 + MCU + TBOX bsp/app | 999 MiB（98%） |
| `v1.25.11-201025` | [cs75plus-2020-1.5T-201025](https://gitee.com/a10463981/cs75plus-2020-1.5T-201025) | **完整原厂 RAR** 11 分卷 + 说明书 PDF | 988 MiB（96%） |
| **4G 修复包** | [cs75plus-2020-1.5T-netfix](https://gitee.com/a10463981/cs75plus-2020-1.5T-netfix) | 完整修复包 2 分卷（`CoagentUpgrade.zip`） | 101.3 MiB（10%）|

> 仍需注意：因单仓 1 GiB 上限，Gitee 侧每个版本**无法容纳全部组件**（例如 `wecarspeech.zip`、部分 `tbox-os.tar.gz`）。
> 需要**逐字节完整的原厂归档**，请走 [GitHub Releases](https://github.com/a10463981/cs75plus-2020-1.5T/releases)。

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

| Release | OS 版本 | 版本日期 | 组件 | 归档文件 | 说明 |
|---|---|---|---|---|---|
| `v1.25.11-201025` | OS_S311-WT-V8_V1.25.11-201025 | 2020-10-25 | OS+MCU | `CoagentUpgrade_V1.25.11-201025.rar` | **最新版**，精简完整包（含官方 U 盘升级说明书 PDF） |
| `v1.09.00-200512` | OS_S311-WT-V8_V01.09.00-200512 | 2020-05-12 | OS+MCU+TBOX | `CoagentUpgrade_V01.09.00-200512.rar` | 双导航版本（含官方升级说明书 PDF，无语音数据） |
| `v0.98.00-191227` | OS_S311-WT-V8_V00.98.00-191227 | 2019-12-27 | OS+MCU+TBOX+语音 | `OS_S311-WT-V8_V00.98.00-191227.zip`（+ 原厂 RAR） | 组件最全，含语音数据包 |
| `v0.75.00-191016` | OS_S311-WT-V8_V00.75.00-191016 | 2019-10-16 | OS+MCU+TBOX+语音 | `CoagentUpgrade_CS75Plus191016.rar` | 目前最老的原厂底包 |

> **降级提示**：原厂升级程序一般只接受**同版本或更高版本**，已升到 `V1.25.11` 的车机无法用这些包自行回退。

## ❓ 常见问题

**Q：这些包里哪个是补丁包？**
A：**没有补丁包，4 个都是完整包。** 每个包内都带一个完整的 OS 镜像（`update.zip`，0.92–1.04 GB 的厂商加密容器），不是增量补丁。区别只在**组件多少**：`191227` 最全（OS+MCU+TBOX+语音），`201025` 最精简（只有 OS+MCU）。详见 [`docs/版本清单.md`](docs/版本清单.md)。

**Q：我该刷哪个版本？**
A：想跟进最新系统 → `v1.25.11-201025`；要组件完整、稳妥 → `v0.98.00-191227`（191227）；需要双导航系统 → `v1.09.00-200512`。**不确定就刷 `v0.98.00-191227`**，它是这套包里组件最全、验证最充分的一版。

**Q：1.5T 和 2.0T 都能刷吗？**
A：**能。** CS75PLUS 2020 款 1.5T 与 2.0T 使用的是同一套 S311-WT 车机主机（屏幕、主控、MCU 一致），区别仅在动力总成。本仓库固件对两款车型通用。前提：确认你的 OS 版本前缀是 `OS_S311-WT-V8`。

**Q：`.rar` 用什么解压？**
A：Windows 用 [7-Zip](https://www.7-zip.org/) 或 WinRAR；macOS 用 Keka / The Unarchiver；Linux 用 `unrar x 文件名.rar`。归档为**原样备份**，未重新打包，请以本仓库给出的 MD5 校验下载完整性。

**Q：下载速度慢 / 断线？**
A：GitHub Release 附件服务器在境外，可用 [IDM](https://www.internetdownloadmanager.com/)、`aria2c` 或多线程下载器；国内网络建议直接走上面的 Gitee 镜像（Gitee 目前仅承载 `v0.98.00-191227`）。

```bash
aria2c -x 8 -s 8 -k 1M "https://github.com/a10463981/cs75plus-2020-1.5T/releases/download/v0.98.00-191227/OS_S311-WT-V8_V00.98.00-191227.zip"
```

**Q：这包能刷别的车型 / 别的年款吗？**
A：**不可以。** 适用范围仅限 **CS75PLUS 2020 款（1.5T / 2.0T）**。其他年款、其他车系或不同平台（如 `S401`、`S311-WT-V9`）刷入会变砖。刷前务必核对「设置 → 关于」里的 OS 版本前缀。

**Q：刷坏了怎么办？**
A：原厂包可重刷恢复；若完全无法进系统，需进入工程模式（部分版本需专用工具/线缆）或联系 4S 店/原厂服务站。
