import sys 
import main
import pytest

def test_main_with_args(monkeypatch):
    test_args = ['main.py', 'arg1', 'arg2']
    monkeypatch.setattr(sys, 'argv', test_args)

    # Invalid args
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1 