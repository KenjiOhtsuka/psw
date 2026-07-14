import time
import sys
from psw.utils import KeyListener


class Stopwatch:
    def __init__(self, precision: int = 3):
        self.precision = precision
        self.listener = KeyListener()
        
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.running = False
        self.laps = []

    def format_time(self, seconds: float) -> str:
        """秒数を '00 h 00 m 00.000 s' のフォーマットに整形する"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        
        # 指定された精度（小数点以下）で秒数をフォーマット
        seconds_str = f"{s:02.{self.precision}f}"
        # 万が一秒が繰り上がって60.00...になった場合の簡易補正
        if float(seconds_str) >= 60.0:
            seconds_str = f"{0.0:02.{self.precision}f}"
            m += 1
            if m >= 60:
                m = 0
                h += 1

        return f"{h:02d} h {m:02d} m {seconds_str} s"

    def run(self):
        self.start_time = time.time()
        self.running = True
        
        print("Stopwatch started. Press 's' to pause/resume, 'l' to record lap, 'q' to quit.\n")
        # 1行分のスペースをあける（リアルタイム描画用）
        print() 

        try:
            while True:
                if self.running:
                    self.elapsed_time = time.time() - self.start_time
                
                # カーソルを上に戻して、現在の時間を描画
                # \033[F はカーソルを1行上に移動、\033[K は行末までクリア
                sys.stdout.write(f"\033[F\033[K{self.format_time(self.elapsed_time)}\n")
                sys.stdout.flush()

                # キー入力のチェック
                char = self.listener.get_char()
                if char == 'q':
                    break
                elif char == 's':
                    if self.running:
                        # 一時停止
                        self.elapsed_time = time.time() - self.start_time
                        self.running = False
                    else:
                        # 再開
                        self.start_time = time.time() - self.elapsed_time
                        self.running = True
                elif char == 'l':
                    if self.running:
                        lap_num = len(self.laps) + 1
                        lap_str = f"  Lap #{lap_num:02d}: {self.format_time(self.elapsed_time)}"
                        self.laps.append(lap_str)
                        # 一旦現在の時間表示の下にラップを挿入するために、描画位置を調整
                        print(lap_str)
                        print() # 次の時間描画のための空行

                # CPU負荷を下げるためのウェイト（ミリ秒精度に合わせて調整）
                # 精度が高い場合は更新頻度を上げ、低い場合は下げる
                sleep_time = 0.01 if self.precision > 2 else 0.05
                time.sleep(sleep_time)

        finally:
            self.listener.close()
            
        # 終了時のまとめ表示
        print(f"\n--- Finished ---")
        print(f"Total Time: {self.format_time(self.elapsed_time)}")
        if self.laps:
            print("Laps:")
            for lap in self.laps:
                print(lap)