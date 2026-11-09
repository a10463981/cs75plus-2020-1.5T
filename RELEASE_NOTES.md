## CS75PLUS 2020款（1.5T / 2.0T）车机系统镜像 v1.0.0 (S311-WT)

长安 CS75PLUS 2020 款（1.5T / 2.0T，同为 S311-WT 平台）车机原厂升级包完整镜像备份，平台 **S311-WT / OS_S311-WT-V8**。

### 📦 下载文件

**原厂整包（推荐，一个文件搞定）**

| 文件 | 大小 | MD5 | SHA256 |
|---|---|---|---|
| `OS_S311-WT-V8_V00.98.00-191227.zip` | 1.10 GiB | `659985d992dcfc64705771f8eb093aff` | `187939a54fde57c08ffc58cbb5fc750a2fed59511d874e7ff24ea716f139896f` |

解压后得到完整 `CoagentUpgrade/` 目录，直接把该文件夹拷到 U 盘根目录即可刷机（整包已通过 CRC 完整性校验）。

**整包内含组件**

| 文件 | 组件 | 大小 | MD5 |
|---|---|---|---|
| `CoagentUpgrade/Os/update.zip` | 系统 OS 镜像 | 956 MB | `e4751da5f1f7ec31f85332dce422573b` |
| `CoagentUpgrade/Mcu/McuAppUpdate.img` | MCU 固件 | 470 KB | `6007ec4ddd5d398c10ae9bdb66f9608d` |
| `CoagentUpgrade/Tbox/tbox-os.tar.gz` | TBOX 系统 | 95.5 MB | `ead3557546d0811b823dfb496298aca1` |
| `CoagentUpgrade/Tbox/tbox-bsp.tar.gz` | TBOX BSP | 5.5 MB | `b05b97dc59c47da16c864d09d7d07060` |
| `CoagentUpgrade/Tbox/tbox-app.tar.gz` | TBOX 应用 | 393 KB | `5f5aba5ce584e5a517eac02eaf2b55b0` |
| `CoagentUpgrade/SoundData/wecarspeech.zip` | 讯飞语音数据 | 67 MB | `5d12c4c2541171924f1bcb15d1db20bf` |

### 🔧 版本信息

- OS：`OS_S311-WT-V8_V00.98.00-191227`（2019-12-27）
- MCU：`MC_V8_S311_V0.68C_191220`（2019-12-20）
- TBOX：os `0.1.9.23` / bsp `0.4.7.51` / app `5.67s.46`（2019-12-12，buildTime=20191212）

### 📥 刷机方法

1. U 盘格式化为 **FAT32**（NTFS/exFAT 部分车机不识别）；
2. 解压 `OS_S311-WT-V8_V00.98.00-191227.zip`，把里面整个 **`CoagentUpgrade/` 文件夹**复制到 U 盘**根目录**（不要多套一层文件夹），最终结构：

```
U盘根目录/
└── CoagentUpgrade/
    ├── Os/          update.zip + MD5.txt + os_versions.txt
    ├── Mcu/         McuAppUpdate.img + MD5.txt + mcu_versions.txt
    ├── Tbox/        tbox-os.tar.gz + tbox-bsp.tar.gz + tbox-app.tar.gz + md5.txt + tbox_version.txt
    └── SoundData/   wecarspeech.zip + md5.txt + wecarspeechMd5 + sound_data_versions.txt
```

3. 车辆 ACC ON（不点火），插入 U 盘，等待车机弹出升级提示 → 确认；
4. **升级过程禁止断电、禁止拔 U 盘**，约 10~20 分钟；
5. 完成后在「设置 → 关于」确认版本为 `V00.98.00-191227`。

> ⚠️ 适用于 CS75PLUS 2020 款 **1.5T 与 2.0T**（同为 S311-WT 平台）：刷前请确认 OS 版本前缀为 `OS_S311-WT-V8`，前缀不符（其他年款 / S401 / S311-WT-V9 等）请勿刷入，否则有变砖风险。
> ⚠️ 原厂升级程序会校验 `MD5.txt`，文件不匹配会自动中止，不会写入。
> ⚠️ 本镜像为非官方备份，固件版权归原厂所有，仅供车主个人设备恢复使用。

### 📚 文档

- [刷机与升级说明](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/刷机与升级说明.md)
- [MD5 校验表](https://github.com/{{OWNER}}/{{REPO}}/blob/main/MD5SUMS.txt)
- [TBOX 历史发版记录](https://github.com/{{OWNER}}/{{REPO}}/blob/main/docs/TBOX-发版记录.md)
