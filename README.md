# yeohphan.github.io — 个人 IPTV 订阅源

> 本仓库仅存放个人使用的 **IPTV m3u 播放列表**，供 APTV / TiviMate / IPTV Pro 等播放器订阅导入。

## ⚠️ 仓库转型说明

**影视仓 / TVBox 订阅源已于 2026-09 起移除**（原 `YingshicangStreams/` 目录及相关配置不再维护，所有旧订阅链接已失效）。本仓库现仅保留 IPTV 直播源。

## 文件清单

| 文件 | 频道数 | 说明 | 适用范围 |
|---|---|---|---|
| `IPTV/Garyshare.m3u` | 2050 | 国际综合源（含央视/卫视/4K/体育/儿童等分组），缓存自第三方公开订阅，EPG 见文件头 | 公网通用 |
| `IPTV/GuangdongIPTV.m3u` | 199 | 广东 IPTV 组播源，地址为内网 UDP→HTTP 代理（`192.168.1.10`），EPG 为内网服务 | **仅本人家中网络**，公网无效 |

## 订阅地址（raw 直链）

```
https://raw.githubusercontent.com/YeohPhan/yeohphan.github.io/main/IPTV/Garyshare.m3u
https://raw.githubusercontent.com/YeohPhan/yeohphan.github.io/main/IPTV/GuangdongIPTV.m3u
```

## 更新规范

1. 单文件变更单条提交，提交信息写明变更内容（如 `chore(iptv): 更新频道列表`），不使用空泛信息。
2. 更新 m3u 前先本地校验：

```bash
python3 scripts/validate_m3u.py IPTV/Garyshare.m3u IPTV/GuangdongIPTV.m3u
```

3. `Garyshare.m3u` 为第三方源缓存，如需跟随上游更新请保留原始行结构，避免产生无谓 diff。

## 免责声明

- 频道地址来自公开免费源及自建内网服务，**仅供个人学习与测试**，请勿用于商业用途或公开传播。
- 广东组播源属运营商网络内内容，公网地址对他人无效；请自行评估再分发风险。
- 所有流地址随时可能失效，本仓库不保证可用性、不承担因使用产生的任何责任。
- 若内容涉及侵权，请联系仓库所有者删除。
