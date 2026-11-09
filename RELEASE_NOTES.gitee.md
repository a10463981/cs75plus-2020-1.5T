## CS75PLUS 2020款（1.5T / 2.0T）车机系统镜像 — OS_S311-WT-V8_V00.98.00-191227（Gitee 分卷版）

长安 CS75PLUS 2020 款（1.5T / 2.0T，同属 **S311-WT** 平台）车机原厂升级包，OS 系统版本 **OS_S311-WT-V8_V00.98.00-191227**（2019-12-27，组件最全）。

> ℹ️ **本页是 Gitee 分卷版。** Gitee 免费仓库限制「单个附件 ≤ 100MB、单仓库附件总量 ≤ 1GB」，1.10 GiB 整包无法整体上传，因此把 OS 系统包拆成 10 个 96MB 分卷（合并后与原包**逐字节一致**）。
> 📦 本仓库还收录了 **V00.75.00-191016 / V01.09.00-200512（双导航）/ V1.25.11-201025（最新）** 三个版本，因 Gitee 附件配额已满，这些完整包**仅在 GitHub 提供**：https://github.com/a10463981/cs75plus-2020-1.5T/releases

### 📊 版本总览

| 项目 | 版本 | 本页是否包含 |
|---|---|---|
| OS 系统 | `OS_S311-WT-V8_V00.98.00-191227` | ✅ 10 个分卷 |
| MCU | `MC_V8_S311_V0.68C_191220` | ✅ 是 |
| TBOX | build 20191212 / os 0.1.9.23 / bsp 0.4.7.51 / app 5.67s.46 | ⚠️ 仅 bsp + app（`tbox-os.tar.gz` 超配额，去 GitHub 下载） |
| 语音数据 | 20191215（9111782-M58） | ❌ 否（超配额，去 GitHub 下载） |

### 📦 本 Release 附件

| 文件 | 大小 | MD5 | 说明 |
|---|---|---|---|
| `update.zip.000` ~ `update.zip.009` | 共 956 MB | 合并后 `e4751da5f1f7ec31f85332dce422573b` | OS 系统镜像分卷（10 卷） |
| `McuAppUpdate.img` | 470 KB | `6007ec4ddd5d398c10ae9bdb66f9608d` | MCU 固件 |
| `tbox-bsp.tar.gz` | 5.46 MB | `b05b97dc59c47da16c864d09d7d07060` | TBOX BSP |
| `tbox-app.tar.gz` | 393 KB | `5f5aba5ce584e5a517eac02eaf2b55b0` | TBOX 应用 |

> 需要 `tbox-os.tar.gz`（95.5 MB）、`wecarspeech.zip`（67 MB）或**整包一个文件**，请走 GitHub：https://github.com/a10463981/cs75plus-2020-1.5T/releases/tag/v0.98.00-191227

### 🔗 分卷合并方法

把 `update.zip.000` ~ `update.zip.009` 下载到同一目录后：

```bash
# Linux / macOS
cat update.zip.00* > update.zip
md5sum update.zip     # 必须是 e4751da5f1f7ec31f85332dce422573b
```

```bat
:: Windows CMD
copy /b update.zip.000+update.zip.001+update.zip.002+update.zip.003+update.zip.004+update.zip.005+update.zip.006+update.zip.007+update.zip.008+update.zip.009 update.zip
```

**最省事**：7-Zip 右键 `update.zip.000` → `提取到当前文件夹`，自动按序合并。

### 🧩 TBOX（4G 通信模块）版本与更新

✅ **本页包含 TBOX 组件**（bsp + app），刷机时会升级 4G 模块固件；`tbox-os.tar.gz` 请从 GitHub 补齐。

| 项目 | 版本 |
|---|---|
| buildTime | `20191212` |
| TBOX OS | `0.1.9.23` |
| TBOX BSP | `0.4.7.51` |
| TBOX APP | `5.67s.46` |

**本次 TBOX 更新要点**（摘自包内 `Tbox/ReleaseNote.md` 原厂原文）：

- **`2019/12/12 [S311]` APP 5.67s**：修复点熄火时间与实际时间有偏差；心跳包上传 GPS 时不再把车速组进 5/100
- **`2019/12/12 [S401]` APP 5.67s**：同上（S401 分支）
- `2019/11/29` APP 5.65s：解决大数据开启时远程开空调超时未反馈 TSP；支持 8/1、8/2、8/3 压缩 tlv

> 完整历史（含 OS / BSP / APP 逐条变更）见 [TBOX 历史发版记录](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/TBOX-发版记录.md)。

### 📥 刷机步骤

1. U 盘格式化为 **FAT32**；
2. 在 U 盘根目录建 `CoagentUpgrade/`，按需放入 `Os/`（合并后的 update.zip）、`Mcu/`、`Tbox/`、`SoundData/`；
3. 车辆 ACC ON（不点火），插入 U 盘 → 车机点「**系统升级**」→「**USB 升级**」→ 一键安装；
4. **升级约 10 分钟，全程禁止断电、禁止拔插 U 盘**；
5. 升级后进「系统设置 → 恢复出厂设置」。

### 📚 相关文档

| 文档 | 内容 |
|---|---|
| [刷机与升级说明](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/刷机与升级说明.md) | U 盘结构、升级步骤、工程模式、常见故障排查 |
| [MD5 校验表](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/MD5SUMS.txt) | 全部镜像与组件的校验值 |
| [版本清单](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/版本清单.md) | 4 个版本的新旧、补丁/完整判定、组件差异、该刷哪个 |
| [TBOX 历史发版记录](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/TBOX-发版记录.md) | 原厂 TBOX 全量发版说明（2019-04 ~ 2019-12） |

### ⚠️ 适用与风险

- 仅适用于 **CS75PLUS 2020 款 1.5T / 2.0T（S311-WT 平台）**，刷前请确认「设置 → 关于」中 OS 版本前缀为 `OS_S311-WT-V8`。
- 原厂升级程序会校验包内 `MD5.txt`，文件不匹配会自动中止，不会写入。
- 非官方备份镜像，固件版权归原厂所有，仅供车主个人设备恢复使用。
