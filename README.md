# cs75plus-2020-1.5T — 长安 CS75PLUS 2020款 1.5T 车机系统镜像库

本仓库用于**备份 / 镜像存放**长安 CS75PLUS 2020 款 1.5T 车型车机（S311-WT 平台，操作系统 `OS_S311-WT-V8`）的原厂升级包，所有镜像以 **GitHub Release 附件**形式提供下载，方便车主自行恢复车机系统。

> ⚠️ 声明：本仓库为非官方镜像备份，与长安汽车及其供应商无关联；固件版权归原厂所有，仅供已购买该车型的车主做个人设备备份/恢复使用，请勿用于商业分发。

---

## 📦 当前版本

| 项目 | 内容 |
|---|---|
| 平台 | S311-WT（Coagent / 德赛西威 车机） |
| OS 版本 | `OS_S311-WT-V8_V00.98.00-191227`（2019-12-27） |
| MCU 版本 | `MC_V8_S311_V0.68C_191220`（2019-12-20） |
| TBOX 版本 | os `0.1.9.23` / bsp `0.4.7.51` / app `5.67s.46`（2019-12-12） |
| 升级包体积 | 约 1.10 GiB（6 个文件） |

## ⬇️ 下载

前往 **[Releases](../../releases/latest)** 页面下载。

### ① 原厂整包（推荐，一个文件搞定）

| 文件 | 大小 | MD5 | SHA256 |
|---|---|---|---|
| [`OS_S311-WT-V8_V00.98.00-191227.zip`](../../releases/latest) | 1.10 GiB | `659985d992dcfc64705771f8eb093aff` | `187939a54fde57c08ffc58cbb5fc750a2fed59511d874e7ff24ea716f139896f` |

解压后得到完整的 `CoagentUpgrade/` 目录（含 MD5 校验文件与版本说明），**直接把整个 `CoagentUpgrade` 文件夹拷到 U 盘根目录**即可刷机，无需自行拼装。

> 包内附带 `__MACOSX/` 目录是 macOS 打包残留，可忽略/删除，不影响升级。

### ② 包内文件清单（整包已含，无需单独下载）

| 文件 | 组件 | 大小 | MD5 |
|---|---|---|---|
| `CoagentUpgrade/Os/update.zip` | **系统 OS 镜像**（核心） | 956 MB | `e4751da5f1f7ec31f85332dce422573b` |
| `CoagentUpgrade/Mcu/McuAppUpdate.img` | MCU 固件 | 470 KB | `6007ec4ddd5d398c10ae9bdb66f9608d` |
| `CoagentUpgrade/Tbox/tbox-os.tar.gz` | TBOX 系统 | 95.5 MB | `ead3557546d0811b823dfb496298aca1` |
| `CoagentUpgrade/Tbox/tbox-bsp.tar.gz` | TBOX BSP | 5.5 MB | `b05b97dc59c47da16c864d09d7d07060` |
| `CoagentUpgrade/Tbox/tbox-app.tar.gz` | TBOX 应用 | 393 KB | `5f5aba5ce584e5a517eac02eaf2b55b0` |
| `CoagentUpgrade/SoundData/wecarspeech.zip` | 讯飞语音数据包 | 67 MB | `5d12c4c2541171924f1bcb15d1db20bf` |

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
├── docs/
│   ├── 刷机与升级说明.md      # U盘升级 / 工程模式 / 排错
│   └── TBOX-发版记录.md       # TBOX 模块历史发版说明（原厂原文）
└── scripts/
    └── upload-release.sh     # 一键建库 + 发布 Release 的维护脚本
```

> 镜像文件**不入 git 仓库**（体积过大），统一放在 Release 附件里；仓库仅保存文档与校验表。

## 🗂️ 版本历史

| Release | OS 版本 | 日期 | 说明 |
|---|---|---|---|
| `v1.0.0` | OS_S311-WT-V8_V00.98.00-191227 | 2019-12-27 | 首次镜像归档，含 OS + MCU + TBOX + 语音包全套 |

## ❓ 常见问题

**Q：下载速度慢 / 断线？**
A：Release 附件服务器在境外。可用 [IDM](https://www.internetdownloadmanager.com/)、`aria2c` 或多线程下载器提高速度：

```bash
aria2c -x 8 -s 8 -k 1M "https://github.com/你的用户名/cs75plus-2020-1.5T/releases/download/v1.0.0/update.zip"
```

**Q：这包能刷别的车型吗？**
A：**不可以。** 仅适用于 CS75PLUS 2020 款 1.5T（S311-WT 平台）。平台不符会导致车机变砖，请先在「设置 → 关于」确认 OS 版本号前缀为 `OS_S311-WT-V8`。

**Q：刷坏了怎么办？**
A：原厂包可重刷恢复；若完全无法进系统，需进入工程模式（部分版本需专用工具/线缆）或联系 4S 店/原厂服务站。
