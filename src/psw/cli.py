import argparse
import sys


def main():
    # 親パーサーの設定（プログラム全体のヘルプや基本情報を定義）
    parser = argparse.ArgumentParser(
        description="PSW - Python Stop Watch & Timer CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # サブコマンド（start / timer）を管理するパーサーを追加
    subparsers = parser.add_subparsers(
        dest="command", 
        required=True, 
        help="Subcommands"
    )

    # ---------------------------------------------------------
    # 1. 'start' (Stopwatch) サブコマンドの設定
    # ---------------------------------------------------------
    parser_start = subparsers.add_parser(
        "start", 
        help="Start the stopwatch"
    )
    parser_start.add_argument(
        "-p", "--precision",
        type=int,
        default=3,
        help="Decimal places for seconds (default: 3)"
    )

    # ---------------------------------------------------------
    # 2. 'timer' サブコマンドの設定
    # ---------------------------------------------------------
    parser_timer = subparsers.add_parser(
        "timer", 
        help="Start the countdown timer"
    )
    # 時間指定（例: 5m, 30s, 1h 30m など可変長の引数を受け取る）
    parser_timer.add_argument(
        "duration",
        nargs="+",
        help="Duration for the timer (e.g., '5m 30s', '1h', '45s')"
    )
    parser_timer.add_argument(
        "-p", "--precision",
        type=int,
        default=3,
        help="Decimal places for seconds (default: 3)"
    )
    parser_timer.add_argument(
        "-r", "--repeat",
        nargs="?",      # optional
        const=-1,       # -1 when only `-r` is used without scceeding number
        default=1,
        type=int,       # Recognize value as Integer when specified
        help="Repeat the timer. Use '-r' for infinite loop, or '-r N' to repeat N times."
    )
    parser_timer.add_argument(
        "-m", "--mute",
        action="store_true",
        help="Mute the terminal bell (\a) alert sound when the timer ends"
    )

    args = parser.parse_args()

    # 各コマンドに応じた処理の分岐
    if args.command == "start":
        try:
            from psw.stopwatch import Stopwatch
            # ストップウォッチの初期化と実行
            sw = Stopwatch(precision=args.precision)
            sw.run()
        except ImportError:
            print("[Error] 'stopwatch.py' is not implemented yet.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "timer":
        try:
            from psw.timer import Timer
            # タイマーの初期化と実行
            timer = Timer(
                duration_strings=args.duration,
                precision=args.precision,
                repeat=args.repeat,
                mute=args.mute
            )
            timer.run()
        except ImportError:
            print("[Error] 'timer.py' is not implemented yet.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()