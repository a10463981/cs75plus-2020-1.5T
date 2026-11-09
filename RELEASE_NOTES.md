## CS75PLUS 2020款（1.5T / 2.0T）车机系统镜像 — OS_S311-WT-V8_V00.98.00-191227

长安 CS75PLUS 2020 款（1.5T / 2.0T，同属 **S311-WT** 平台）车机原厂升级包，OS 系统版本 **OS_S311-WT-V8_V00.98.00-191227**（2019-12-27，组件最全）。

### 📊 版本总览

| 项目 | 版本 | 本包是否包含 |
|---|---|---|
| OS 系统 | `OS_S311-WT-V8_V00.98.00-191227` | ✅ 是 |
| MCU | `MC_V8_S311_V0.68C_191220` | ✅ 是 |
| TBOX | build 20191212 / os 0.1.9.23 / bsp 0.4.7.51 / app 5.67s.46 | ✅ 是 |
| 语音数据 | 20191215（9111782-M58） | ✅ 是 |

### 📦 本 Release 附件

| 文件 | 大小 | MD5 | 说明 |
|---|---|---|---|
| `OS_S311-WT-V8_V00.98.00-191227.zip` | 1,178,966,143 B (1.10 GiB) | `659985d992dcfc64705771f8eb093aff` | 整包 ZIP（解压即用） |
| `CoagentUpgrade_CS75Plus191227.rar` | 1,170,114,650 B (1.09 GiB) | `7bc21686331c873d00022da0e822ac49` | 原厂 RAR 原样备份（与 ZIP 同源） |

> 解压得到完整的 `CoagentUpgrade/` 目录。Windows 建议用 [7-Zip](https://www.7-zip.org/) / WinRAR，Linux 用 `unrar x OS_S311-WT-V8_V00.98.00-191227.zip`。

### 🧩 TBOX（4G 通信模块）版本与更新

✅ **本包含 TBOX 组件**，刷机时会一并升级 4G 模块固件。

| 项目 | 版本 |
|---|---|
| buildTime | `20191212` |
| TBOX OS | `0.1.9.23` |
| TBOX BSP | `0.4.7.51` |
| TBOX APP | `5.67s.46` |

| 文件 | 大小 | MD5 |
|---|---|---|
| `tbox-os.tar.gz` | 95.5 MB | `ead3557546d0811b823dfb496298aca1` |
| `tbox-bsp.tar.gz` | 5.46 MB | `b05b97dc59c47da16c864d09d7d07060` |
| `tbox-app.tar.gz` | 393.4 KB | `5f5aba5ce584e5a517eac02eaf2b55b0` |

**本次 TBOX 更新要点**（摘自包内 `Tbox/ReleaseNote.md` 原厂原文，最新在前）：

- **`2019/12/12 [S311]` APP 5.67s**：修复点熄火时间与实际时间有偏差；心跳包上传 GPS 时不再把车速组进 5/100
- **`2019/12/12 [S401]` APP 5.67s**：同上（S401 分支）
- `2019/11/29` APP 5.65s：解决大数据开启时远程开空调超时未反馈 TSP；支持 8/1、8/2、8/3 压缩 tlv

> 完整历史（含 OS / BSP / APP 逐条变更）见 [TBOX 历史发版记录](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/TBOX-发版记录.md)。


### 🔧 包内组件

```
CoagentUpgrade/
├── Mcu/McuAppUpdate.img      481,013 B
├── Os/update.zip           1,002 MB    (MD5 e4751da5f1f7ec31f85332dce422573b)
├── SoundData/wecarspeech.zip  67 MB    (MD5 5d12c4c2541171924f1bcb15d1db20bf)
└── Tbox/tbox-{os,bsp,app}  ~106 MB
```

### 📥 刷机步骤

1. U 盘格式化为 **FAT32**；
2. 解压 RAR，把里面的 **`CoagentUpgrade/` 整个文件夹**放到 U 盘**根目录**（不要多套一层）；
3. 车辆 ACC ON（不点火），插入 U 盘 → 车机点「**系统升级**」→「**USB 升级**」；
4. 核对车机显示的 OS / MCU 版本与本页一致后，点「一键安装」确认；
5. **升级约 10 分钟，全程禁止断电、禁止拔插 U 盘**，完成后自动重启；
6. 升级后进「系统设置 → 恢复出厂设置」。

### 📚 相关文档

| 文档 | 内容 |
|---|---|
| [刷机与升级说明](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/刷机与升级说明.md) | U 盘结构、升级步骤、工程模式、常见故障排查 |
| [MD5 校验表](https://github.com/{{OWNER}}/{{REPO}}/blob/main/MD5SUMS.txt) | 全部镜像与组件的校验值 |
| [版本清单](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/版本清单.md) | 4 个版本的新旧、补丁/完整判定、组件差异、该刷哪个 |
| [TBOX 历史发版记录](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/TBOX-发版记录.md) | 原厂 TBOX 全量发版说明（2019-04 ~ 2019-12） |

### ⚠️ 适用与风险

- 仅适用于 **CS75PLUS 2020 款 1.5T / 2.0T（S311-WT 平台）**，刷前请确认「设置 → 关于」中 OS 版本前缀为 `OS_S311-WT-V8`。
- 原厂升级程序会校验包内 `MD5.txt`，文件不匹配会自动中止，不会写入。
- 非官方备份镜像，固件版权归原厂所有，仅供车主个人设备恢复使用。

> 📝 本 Release 原名 `v1.0.0`，为与其它版本统一（`v<OS版本号>-<日期>`）已更名为 `v0.98.00-191227`，旧链接失效。
> 完整分析见 [版本清单](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/版本清单.md)。
