import sys
from unittest.mock import patch, MagicMock
import pytest
from psw.cli import main


# 1. 存在しないサブコマンドや不正なオプションが指定された場合のテスト
def test_cli_invalid_command():
    # 引数に存在しないコマンド 'invalid_cmd' を渡す模擬設定
    with patch.object(sys, "argv", ["psw", "invalid_cmd"]):
        # argparseはパースに失敗すると SystemExit(code=2) を発生させます
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 2


# 2. 'start' (Stopwatch) コマンドのパーステスト
@patch("psw.stopwatch.Stopwatch")
def test_cli_start_command(mock_stopwatch):
    # 'psw start -p 2' が入力されたと仮定
    with patch.object(sys, "argv", ["psw", "start", "-p", "2"]):
        main()
        
        # Stopwatchクラスが正しい引数でインスタンス化され、run()が実行されたか検証
        mock_stopwatch.assert_called_once_with(precision=2)
        mock_stopwatch.return_value.run.assert_called_once()


# 3. 'timer' コマンドのパーステスト
@patch("psw.timer.Timer")
def test_cli_timer_command(mock_timer):
    # 'psw timer 1m 30s -p 1 -r -m' が入力されたと仮定
    with patch.object(sys, "argv", ["psw", "timer", "1m", "30s", "-p", "1", "-r", "-m"]):
        main()
        
        # Timerクラスが各オプションを正しく受け取ってインスタンス化されたか検証
        mock_timer.assert_called_once_with(
            duration_strings=["1m", "30s"],
            precision=1,
            repeat=True,
            mute=True
        )
        mock_timer.return_value.run.assert_called_once()


# 4. 'timer' コマンドで count オプションが指定された場合のパーステスト
@patch("psw.timer.Timer")
def test_cli_timer_count_option(mock_timer):
    # 'psw timer 10s -r 3' が入力されたと仮定
    with patch.object(sys, "argv", ["psw", "timer", "10s", "-r", "3"]):
        main()
        
        mock_timer.assert_called_once_with(
            duration_strings=["10s"],
            precision=3,  # デフォルト値
            repeat=3,     # 3 times repeat
            mute=False    # デフォルト値
        )