"""鲜记的启动入口。

在 PyCharm 里右键运行这个文件即可；也可以在终端执行：

    python run.py

默认打开 http://127.0.0.1:8765 ，桌面端和手机（同一局域网）都可以访问。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fridge.config import APP_NAME, APP_SUBTITLE, DEFAULT_DB_PATH, HOST, PORT
from fridge.web import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xianji",
        description=f"{APP_NAME} · {APP_SUBTITLE}：本地冰箱库存与临期提醒。",
    )
    parser.add_argument(
        "--host",
        default=HOST,
        help="监听地址，默认 127.0.0.1；要让同一 Wi-Fi 的手机访问可填 0.0.0.0",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help=f"端口，默认 {PORT}",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="SQLite 数据库文件路径",
    )
    parser.add_argument(
        "--no-demo",
        action="store_true",
        help="第一次启动时不写入示例冰箱（从空白开始）",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="启动后不自动打开浏览器",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="在错误页显示 traceback，仅用于开发",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    args = build_parser().parse_args(argv)
    try:
        serve(
            db_path=args.db,
            host=args.host,
            port=args.port,
            seed_demo=not args.no_demo,
            debug=args.debug,
            open_browser=not args.no_browser,
        )
    except OSError as exc:
        print(f"启动失败：{exc}", file=sys.stderr)
        print("如果端口被占用，可以换一个端口：python run.py --port 8766", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
