import pytest

import os
import sys

# Get the absolute path of the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from files import cmdutils

def test_help(capsys):
    args = ["-h"]
    assert cmdutils.cmd_main(args) == -1
    
    captured = capsys.readouterr()
    assert help in captured.out

def test_help_2(capsys):
    args = ["--help"]
    assert cmdutils.cmd_main(args) == -1
    
    captured = capsys.readouterr()
    assert help in captured.out

def test_help_3(capsys):
    args = ["-help"]
    assert cmdutils.cmd_main(args) == -1
    
    captured = capsys.readouterr()
    assert help in captured.out

def test_help_4(capsys):
    args = ["--h"]
    assert cmdutils.cmd_main(args) == -1
    
    captured = capsys.readouterr()
    assert help in captured.out

def test_help_5(capsys):
    args = []
    assert cmdutils.cmd_main(args) == -1
    
    captured = capsys.readouterr()
    assert help in captured.out

help = '''
Usage: python main.py [options]

Options:
  -h, --help, -help, --h       Show this help message and exit
  -f <emulator>                Specify the input emulator
  -t <emulator>                Specify the output emulator
  -i <input_file>              Specify the input file(s)
  -o <output_file>             Specify the output file
  -r <rom_location>            Rom to extract name from

Notes:
    -r option not necesarily required, but BizHawk could switch out underscores for spaces
    If no -o is specified, the output file will be the same name as the input file
    
Required options:
    -f <emulator>               Specify the input emulator
    -t <emulator>               Specify the output emulator
    -i <input_file>             Specify the input file(s)

Supported emulators (valid options):
    - Ares - ares, are 
    - bizhawk - BizHawk, biz, EmuHawk
    - retroarch - retroarch, ret
    - More to be added in the future

Example:
    python main.py -f ares -t bizhawk -i 'Dr. Mario 64 (USA).eeprom' -o 'Dr. Mario 64 (USA).SaveRAM' -r 'Dr. Mario 64 (USA).z64'
'''