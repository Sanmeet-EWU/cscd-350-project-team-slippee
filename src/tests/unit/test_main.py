import sys
import pytest
import importlib
  # import once so it's available in sys.modules


def test_main_with_invalid_args(monkeypatch):
    test_args = ['main.py', 'arg1', 'arg2']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main
    

    # Invalid args
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1 

def test_main_with_1_valid_args(monkeypatch):
    
    test_args = ['main.py', '-f', 'test_emu']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main
    

    # Invalid args
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1 

#############
# Test Help #
#############
def test_help_from_main(capsys, monkeypatch):
    
    test_args = ['main.py', '-h']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main
    importlib.reload(main)  

    # Invalid args
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1 

    captured = capsys.readouterr()
    assert "Usage: python main.py" in captured.out
    assert "-f <emulator>" in captured.out

###############################
# Test Main with invalid args #
###############################
def test_main_with_no_args(monkeypatch):
    test_args = ['main.py']

    monkeypatch.setattr(sys, 'argv', test_args)
    
    import main
    importlib.reload(main)  

    # Invalid args
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1

def test_main_with_invalid_input_emu(capsys, monkeypatch):
    test_args = ['main.py', '-t']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main    
    importlib.reload(main)  


    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1

    captured = capsys.readouterr()
    assert f"No input emulator specified" in captured.out.strip()

def test_main_with_invalid_output_emu(capsys, monkeypatch):
    test_args = ['main.py', '-f', 'ares']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main

    importlib.reload(main)  

    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1

    #captured = capsys.readouterr()
    #assert "No output emulator specified" in captured.out.strip()

def test_main_with_invalid_input_file(capsys, monkeypatch):
    test_args = ['main.py', '-f', 'ares', '-t', 'bizhawk']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main

    importlib.reload(main)  

    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.type == SystemExit
    assert exc_info.value.code == -1

    captured = capsys.readouterr()
    assert "No input file specified" in captured.out.strip()

def test_main_with_invalid_output_file(capsys, monkeypatch):
    test_args = ['main.py', '-f', 'ares', '-t', 'bizhawk', '-i', 'input_file']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main

    importlib.reload(main)  

    main.main()
    
    captured = capsys.readouterr()
    assert "File Does Not Exist" in captured.out.strip()

def test_main_with_invalid_rom_location(capsys, monkeypatch):
    test_args = ['main.py', '-f', 'ares', '-t', 'bizhawk', '-i', 'input_file', '-r', 'output_file']
    monkeypatch.setattr(sys, 'argv', test_args)

    import main

    importlib.reload(main)  

    main.main()

    captured = capsys.readouterr()
    assert "Rom location does not exist" in captured.out.strip()

def test_main_with_valid_args(capsys, monkeypatch):
    test_args = ['main.py', '-f', 'ares', '-t', 'bizhawk', '-i', './src/tests/tests.eeprom', '-o', './src/output/tests.SaveRAM', '-r', './src/tests/tests.z64'] 
    monkeypatch.setattr(sys, 'argv', test_args)

    import main

    importlib.reload(main)  

    # Valid args
    main.main()
    captured = capsys.readouterr()

    assert "Input Emulator: Ares" in captured.out.strip()
    assert "Output Emulator: BizHawk" in captured.out.strip()
