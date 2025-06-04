
import os
import sys

# Get the absolute path of the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import pytest
from emulators import ares

class TestEmu:
    ###################
    # Test Endian Fix #
    ###################
    def test_endian_fix(self):
        emu = ares.Ares()
        assert emu.endian_fix(b"\xef\xbe\xad\xde") == b"\xde\xad\xbe\xef"
        assert emu.endian_fix(b"") == b""
        assert emu.endian_fix(b"\x00\x00\x00\x00") == b"\x00\x00\x00\x00"
        assert emu.endian_fix(b"\x01\x02\x03\x04") == b"\x04\x03\x02\x01"
    
    def test_endian_fix_invalid_length(self):
        emu = ares.Ares()
        assert emu.endian_fix(b"\x01") == b""
    
    def test_endian_fix_non_bytes(self):
        emu = ares.Ares()
        assert emu.endian_fix("not byte") == b""