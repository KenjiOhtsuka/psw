import sys

# OS判定
is_windows = sys.platform.startswith("win")

if is_windows:
    import msvcrt
else:
    import select
    import tty
    import termios


class KeyListener:
    """ノンブロッキングでキー入力を監視するクラス"""

    def __init__(self):
        self.old_settings = None
        if not is_windows and sys.stdin.isatty():
            # ターミナルの標準入力設定を保存
            self.old_settings = termios.tcgetattr(sys.stdin)

    def get_char(self) -> str:
        """押されたキーを1文字取得する（押されていなければ空文字を返す）"""
        if is_windows:
            if msvcrt.kbhit():
                # Windowsのキー取得
                try:
                    char = msvcrt.getch().decode("utf-8").lower()
                    return char
                except UnicodeDecodeError:
                    return ""
            return ""
        else:
            # macOS/Linuxのキー取得（cbreakモードに一時的に切り替える）
            try:
                tty.setcbreak(sys.stdin.fileno())
                # 読み込み可能か確認（タイムアウト0秒）
                dr, _, _ = select.select([sys.stdin], [], [], 0)
                if dr:
                    return sys.stdin.read(1).lower()
                return ""
            finally:
                # ターミナル設定を元に戻す
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def close(self):
        """終了処理（ターミナルの設定を完全に復元）"""
        if not is_windows and self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)