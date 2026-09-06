#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_m3u.py — 校验 m3u 播放列表文件结构。

用法:
    python3 scripts/validate_m3u.py [文件1.m3u 文件2.m3u ...]
    python3 scripts/validate_m3u.py                 # 默认校验 IPTV/ 下所有 *.m3u

校验项:
    1. 文件可解码（UTF-8）
    2. 无 null / undefined 等坏行
    3. 每个 #EXTINF 之后必须跟随一条有效流地址
    4. 流地址协议须在白名单内（http/https/rtp/rtmp/udp）
    5. 文件必须以 #EXTM3U 开头

退出码: 0 = 全部通过; 1 = 存在异常（异常详情打印到 stderr）
"""
import re
import sys
from pathlib import Path

SCHEME_WHITELIST = {"http", "https", "rtp", "rtmp", "udp"}
BAD_TOKENS = {"null", "undefined", "none", "nul"}


def validate(path: Path) -> list[str]:
    """返回异常列表，为空表示通过。"""
    errors = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError) as e:
        return [f"<{path}> 无法按 UTF-8 读取: {e}"]

    if not lines or not lines[0].startswith("#EXTM3U"):
        errors.append(f"<{path}> 首行缺失 #EXTM3U 标记")

    uri_re = re.compile(r"^(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)://")
    extinf_count = 0
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        # 1) 坏行检查
        if stripped.lower() in BAD_TOKENS:
            errors.append(f"<{path}>:{i} 坏行 {stripped!r}")

        # 2) EXTINF 配对检查
        if stripped.startswith("#EXTINF"):
            extinf_count += 1
            j = i  # 1-based；跳过后继 # 注释行
            while j < len(lines) and (lines[j].lstrip().startswith("#") or not lines[j].strip()):
                j += 1
            nxt = lines[j].strip() if j < len(lines) else ""
            if not nxt:
                errors.append(f"<{path}>:{i} EXTINF 后缺失流地址（文件结尾）")
            elif not uri_re.match(nxt):
                errors.append(f"<{path}>:{i} EXTINF 后接非地址行: {nxt[:60]!r}")
            continue

        # 3) 非注释行必须是合法协议地址
        if not stripped.startswith("#"):
            m = uri_re.match(stripped)
            if not m:
                errors.append(f"<{path}>:{i} 无法识别的流地址行: {stripped[:60]!r}")
            elif m.group("scheme").lower() not in SCHEME_WHITELIST:
                errors.append(f"<{path}>:{i} 协议不在白名单: {m.group('scheme')}")

    if not errors:
        print(f"OK  <{path}> 频道数(EXTINF): {extinf_count}")
    return errors


def main() -> int:
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    else:
        targets = sorted(Path("IPTV").glob("*.m3u")) if Path("IPTV").is_dir() else []

    if not targets:
        print("未找到待校验文件。用法: validate_m3u.py <file1.m3u ...>", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for t in targets:
        if not t.is_file():
            all_errors.append(f"<{t}> 文件不存在")
            continue
        all_errors.extend(validate(t))

    if all_errors:
        print(f"\n发现 {len(all_errors)} 处异常:", file=sys.stderr)
        for e in all_errors:
            print(" -", e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
