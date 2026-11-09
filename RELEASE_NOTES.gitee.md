## CS75PLUS 2020款（1.5T / 2.0T）车机系统镜像 V00.98.00-191227 (S311-WT) — Gitee 分卷版

长安 CS75PLUS 2020 款（1.5T / 2.0T，同为 S311-WT 平台）车机原厂升级包镜像，平台 **S311-WT / OS_S311-WT-V8**。

> ℹ️ **本页是分卷版。**
> 📦 本仓库还收录了 **V00.75.00-191016 / V01.09.00-200512（双导航）/ V1.25.11-201025（最新）** 三个版本，因 Gitee 附件配额（单库 1GB）限制，这些完整包**仅在 GitHub 提供**：
> https://github.com/a10463981/cs75plus-2020-1.5T/releases
 Gitee 免费仓库限制「单个附件 ≤ 100MB、单仓库附件总量 ≤ 1GB」，1.10 GiB 的整包无法整体上传，因此把 OS 系统包拆成 10 个 96MB 分卷（合并后与原包逐字节一致）。
> 需要**一个文件直接下载**，或需要 `tbox-os.tar.gz`、`wecarspeech.zip`，请走 GitHub：
> https://github.com/a10463981/cs75plus-2020-1.5T/releases/latest

### 📦 本页附件

| 文件 | 组件 | 大小 | MD5 |
|---|---|---|---|
| `update.zip.000` ~ `update.zip.009` | OS 系统镜像分卷（10 卷） | 共 956 MB | 合并后 `e4751da5f1f7ec31f85332dce422573b` |
| `McuAppUpdate.img` | MCU 固件 | 470 KB | `6007ec4ddd5d398c10ae9bdb66f9608d` |
| `tbox-bsp.tar.gz` | TBOX BSP | 5.5 MB | `b05b97dc59c47da16c864d09d7d07060` |
| `tbox-app.tar.gz` | TBOX 应用 | 393 KB | `5f5aba5ce584e5a517eac02eaf2b55b0` |

> `tbox-os.tar.gz`（95.5 MB）与 `wecarspeech.zip`（67 MB）因 Gitee 附件额度限制未上传，请从 GitHub 获取。

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

合并得到的 `update.zip` 即 `CoagentUpgrade/Os/update.zip`。

### 🔧 版本信息

- OS：`OS_S311-WT-V8_V00.98.00-191227`（2019-12-27）
- MCU：`MC_V8_S311_V0.68C_191220`（2019-12-20）
- TBOX：os `0.1.9.23` / bsp `0.4.7.51` / app `5.67s.46`（2019-12-12）

### 📥 刷机方法

1. U 盘格式化为 **FAT32**；
2. 在 U 盘根目录建立 `CoagentUpgrade/Os/`，把合并好的 `update.zip` 放进去（其余组件按需补 `Mcu/`、`Tbox/`、`SoundData/`）；
3. 车辆 ACC ON（不点火），插入 U 盘，等待车机弹出升级提示 → 确认；
4. **升级过程禁止断电、禁止拔 U 盘**，约 10~20 分钟；
5. 完成后在「设置 → 关于」确认版本为 `V00.98.00-191227`。

> ⚠️ 适用于 CS75PLUS 2020 款 **1.5T 与 2.0T**（同为 S311-WT 平台）：刷前请确认 OS 版本前缀为 `OS_S311-WT-V8`，前缀不符（其他年款 / S401 / S311-WT-V9 等）请勿刷入，否则有变砖风险。
> ⚠️ 原厂升级程序会校验 `MD5.txt`，文件不匹配会自动中止，不会写入。
> ⚠️ 本镜像为非官方备份，固件版权归原厂所有，仅供车主个人设备恢复使用。

### 📚 文档

- [刷机与升级说明](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/刷机与升级说明.md)
- [MD5 校验表](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/MD5SUMS.txt)
- [TBOX 历史发版记录](https://gitee.com/a10463981/cs75plus-2020-1.5T/blob/main/docs/TBOX-发版记录.md)
