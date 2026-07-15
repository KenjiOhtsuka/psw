# パッケージ外から直接 Stopwatch や Timer をインポートできるように公開します。
# 例: from psw import Stopwatch, Timer
from psw.stopwatch import Stopwatch
from psw.timer import Timer

# パッケージのバージョン（pyproject.toml と合わせておくと管理しやすいです）
__version__ = "0.1.0"

# `from psw import *` をした際にインポートされるクラスを指定
__all__ = ["Stopwatch", "Timer"]