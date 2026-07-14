import pytest
from psw.timer import Timer


# 1. 正常な時間パースのテスト
@pytest.mark.parametrize(
    "duration_list, expected_seconds",
    [
        (["10s"], 10.0),
        (["5m"], 300.0),
        (["1h"], 3600.0),
        (["1h", "30m", "15s"], 5415.0),  # 複数引数の組み合わせ
        (["0.5m"], 30.0),                # 小数点
        (["10"], 10.0),                  # 単位なし（デフォルト秒）
    ],
)
def test_parse_duration_success(duration_list, expected_seconds):
    # Timerインスタンスを作成してパース結果を検証
    # (テスト実行時にタイマー自体は動かさないため、ダミーの値を渡します)
    timer = Timer(duration_strings=duration_list, mute=True)
    assert timer.total_seconds == expected_seconds


# 2. 異常な入力に対するテスト
def test_parse_duration_invalid_and_exit():
    # 0秒以下や、解釈不能な文字列だけで実行された場合、
    # プログラムが SystemExit (sys.exit(1)) で終了することを確認します。
    with pytest.raises(SystemExit) as excinfo:
        Timer(duration_strings=["invalid_string"], mute=True)
    
    # 終了コードが 1 であることを検証
    assert excinfo.value.code == 1