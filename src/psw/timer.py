import time
import sys
import re
import os
from psw.utils import KeyListener

is_windows = os.name == "nt" or sys.platform.startswith("win")
if is_windows:
    import winsound

class Timer:
    def __init__(
        self,
        duration_strings: list,
        precision: int = 3,
        repeat: bool = False,
        count: int = None,
        mute: bool = False,
    ):
        self.duration_strings = duration_strings
        self.precision = precision
        self.repeat = repeat
        self.count = count
        self.mute = mute

        self.listener = KeyListener()
        
        # 入力された文字列（['5m', '30s'] など）から合計秒数を算出
        self.total_seconds = self.parse_duration(duration_strings)
        self.remaining_time = self.total_seconds
        
        self.running = False
        self.start_time = 0.0

    def parse_duration(self, duration_strings: list) -> float:
        """
        ['1h', '30m', '45s'] のような入力リストを解析し、合計秒数を返す。
        単位が指定されていない単なる数値は「秒」として扱う。
        """
        total = 0.0
        # 時間パース用の正規表現 (例: "5.5m", "10s", "1h")
        pattern = re.compile(r"^([\d.]+)([hms]?)$")

        for s in duration_strings:
            s = s.strip().lower()
            match = pattern.match(s)
            if not match:
                print(f"[Warning] Could not parse duration part: '{s}'. Ignored.", file=sys.stderr)
                continue
            
            value_str, unit = match.groups()
            try:
                value = float(value_str)
            except ValueError:
                continue

            if unit == "h":
                total += value * 3600
            elif unit == "m":
                total += value * 60
            elif unit == "s" or unit == "":
                total += value

        if total <= 0:
            print("[Error] Total duration must be greater than 0.", file=sys.stderr)
            sys.exit(1)

        return total

    def format_time(self, seconds: float) -> str:
        """秒数を '00 h 00 m 00.000 s' のフォーマットに整形する"""
        if seconds < 0:
            seconds = 0.0
            
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        
        seconds_str = f"{s:02.{self.precision}f}"
        if float(seconds_str) >= 60.0:
            seconds_str = f"{0.0:02.{self.precision}f}"
            m += 1
            if m >= 60:
                m = 0
                h += 1

        return f"{h:02d} h {m:02d} m {seconds_str} s"

    def run_single_timer(self, cycle_num: int = None) -> bool:
        """
        1回分のタイマーカウントダウンを実行する。
        戻り値: True (完走した), False (ユーザーが 'q' で中断した)
        """
        self.remaining_time = self.total_seconds
        self.start_time = time.time()
        self.running = True

        # 進捗タイトルの表示
        if cycle_num is not None:
            print(f"--- Timer Cycle #{cycle_num} ---")
        else:
            print("--- Timer Started ---")
        print("Press 's' to pause/resume, 'q' to quit.\n\n")

        try:
            while self.remaining_time > 0:
                if self.running:
                    # 経過時間を引き、残りの時間を計算
                    elapsed = time.time() - self.start_time
                    self.remaining_time = self.total_seconds - elapsed
                    if self.remaining_time < 0:
                        self.remaining_time = 0.0

                # カーソルを上に戻して、現在の時間を描画
                sys.stdout.write(f"\033[F\033[K{self.format_time(self.remaining_time)}\n")
                sys.stdout.flush()

                if self.remaining_time <= 0:
                    break

                # キー入力チェック
                char = self.listener.get_char()
                if char == 'q':
                    return False
                elif char == 's':
                    if self.running:
                        # 一時停止
                        self.total_seconds = self.remaining_time
                        self.running = False
                    else:
                        # 再開
                        self.start_time = time.time()
                        self.running = True

                sleep_time = 0.01 if self.precision > 2 else 0.05
                time.sleep(sleep_time)

            # タイムアップ時、00:00:00.000を表示させる
            sys.stdout.write(f"\033[F\033[K{self.format_time(0.0)}\n")
            sys.stdout.flush()
            
            # ビープ音の鳴動
            if not self.mute:
                if is_windows:
                    try:
                        # winsound.MessageBeep() は Windows標準のアラート音を鳴らします
                        # (winsound.Beep(1000, 500) で特定の周波数を鳴らすことも可能です)
                        winsound.MessageBeep()
                    except Exception:
                        sys.stdout.write("\a")
                        sys.stdout.flush()
                else:
                    # mac or linux
                    sys.stdout.write("\a")
                    sys.stdout.flush()
                
            print("\nTime's up!")
            return True

        finally:
            # 1回分の表示領域をクリアして改行を整える
            print()

    def run(self):
        try:
            # 1. 回数指定リピートがある場合
            if self.count is not None:
                for i in range(1, self.count + 1):
                    completed = self.run_single_timer(cycle_num=i)
                    if not completed:
                        print("Timer canceled by user.")
                        break
                    # ループ間に少しウェイトを挟む（即座に次が始まって画面が崩れるのを防ぐ）
                    if i < self.count:
                        time.sleep(1)
            
            # 2. 無限リピート（-r）の場合
            elif self.repeat:
                cycle = 1
                while True:
                    completed = self.run_single_timer(cycle_num=cycle)
                    if not completed:
                        print("Timer canceled by user.")
                        break
                    cycle += 1
                    time.sleep(1)

            # 3. 通常の1回切りタイマーの場合
            else:
                completed = self.run_single_timer()
                if not completed:
                    print("Timer canceled by user.")

        finally:
            self.listener.close()