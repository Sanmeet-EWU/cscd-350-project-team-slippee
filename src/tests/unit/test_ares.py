
import os
import sys

# Get the absolute path of the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import pytest
from emulators import ares

class TestAres:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_ares = ares.Ares()
        self.inputFiles = ["src/tests/tests.eeprom",
                           "src/tests/tests1.eeprom",
                           "src/tests/tests2.ram",
                           "src/tests/tests.flash",
                           "src/tests/tests.pak",
                           "src/tests/tests.ram"]
    
    def check_endianess(self, file):
        if len(file) % 4 != 0:
            return False
        
        for i in range(len(file) // 4):
            if not file[i  * 4: (i + 1) * 4] == b"\xef\xbe\xad\xde":
                return False
        return True
        
    def readin_fortests(self, file):
        try:
            with open(file, "rb") as inp:
                return inp.read()
        except FileNotFoundError:
            return b"FileNotFound"
        except Exception as e:
            return str(e).encode()
    
    ################
    #              #
    # Basic Tests  #
    #              #
    ################

    # Test input file list validation
    def test_set_valid_input(self):
        assert self.test_ares.set_input_file(self.inputFiles) == True
        assert self.test_ares.get_input_file() == self.inputFiles
    
    def test_set_invalid_input(self):
        assert self.test_ares.set_input_file("Not a List") == False
        assert self.test_ares.get_input_file() == []
    
    # Test output file validation
    def test_set_valid_outfile(self):
        file = "somefile"
        assert self.test_ares.set_outfile(file) == True
        assert self.test_ares.get_outfile() == file

    def test_set_valid_outfile(self):
        assert self.test_ares.set_outfile(0xdeadbeef) == False
        assert self.test_ares.get_outfile() == ""

    # Test Endian Fix
    def test_endian_fix(self):
        file = self.readin_fortests(self.inputFiles[0])
        endian_fixed_file = self.test_ares.endian_fix(file)
        
        assert endian_fixed_file[:8] == b" 215): B"
        assert self.check_endianess(endian_fixed_file[8:]) == True

    ################################
    #                              #
    # Tests for ares.split_file    #
    #                              #
    ################################ 

    #########################################
    # Input Validation Tests for split_file #
    #########################################  
    def test_split_file_invalid_input(self):
        file = "Not a List"

        file_dictionary = self.test_ares.split_file(file)
        assert file_dictionary == {"error": "Input is not a list", "file": file}
        assert self.test_ares.get_outfile() == ""
    
    def test_split_file_no_input(self):
        file = []

        file_dictionary = self.test_ares.split_file(file)
        assert file_dictionary == {"error": "No files provided", "file": file}
        assert self.test_ares.get_outfile() == ""
    
    def test_split_file_empty_input(self):
        file = [""]
        
        file_dictionary = self.test_ares.split_file(file)
        assert file_dictionary['error'] == "File type not recognized"
        assert file_dictionary['file'] == file[0]
        assert self.test_ares.get_outfile() == ""

    def test_split_file_invalid_file(self):
        file = [123]

        file_dictionary = self.test_ares.split_file(file)
        assert file_dictionary == {"error": "File is not a string", "file": file}
        assert self.test_ares.get_outfile() == ""    
    
    def test_convert_file_invalid(self):
        file = ["src/tests/tests.SaveRAM"]

        file_dictionary = self.test_ares.split_file(file)

        assert file_dictionary['error'] == 'File type not recognized'
        assert file_dictionary["file"] == file

    ####################################
    # Tests for each of the file types #
    ####################################
    def test_split_file_eeprom_512(self):
        file = self.inputFiles[0]

        file_dictionary = self.test_ares.split_file([ file ])
        assert file_dictionary['eeprom'] == self.readin_fortests(file)
    
    def test_split_file_eeprom_2KB(self):
        file = self.inputFiles[1]

        file_dictionary = self.test_ares.split_file([ file ])
        assert file_dictionary['eeprom'] == self.readin_fortests(file)
    
    def test_split_file_eeprom_96KB(self):
        file = self.inputFiles[2]

        file_dictionary = self.test_ares.split_file([ file ])
        assert file_dictionary['dram'] == self.readin_fortests(file)
    
    def test_split_file_flash(self):
       
        file = self.inputFiles[3]

        file_dictionary = self.test_ares.split_file([ file ])
        assert file_dictionary['flash'] == self.readin_fortests(file)
    
    def test_split_file_pak(self):
        file = self.inputFiles[4]

        file_dictionary = self.test_ares.split_file([ file ])
        assert file_dictionary['pak'] == self.readin_fortests(file)
    
    def test_split_file_ram(self):
        file = self.inputFiles[5]

        file_dictionary = self.test_ares.split_file([ file ])
        assert file_dictionary['ram'] == self.readin_fortests(file)

    #################################
    # Test File That does not exist #
    #################################
    def test_split_file_nonexistent_file(self):
        file = "thisfiledoesnotexists.txt"

        file_dictionary = self.test_ares.split_file([ file ])

        exception_string = self.readin_fortests(file)

        assert exception_string == b"FileNotFound"
        assert file_dictionary == {'error': 'File type not recognized', 'file': 'thisfiledoesnotexists.txt'}

    ###############################
    # Tests for ares.convert_file #
    ###############################
    def test_convert_file_eeprom_512(self):
        outfile = "test_output"
        file = self.inputFiles[0]

        file_dictionary = self.test_ares.split_file([ file ])

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == True
        assert number == 1

        assert self.readin_fortests(f"src/output/{outfile}.eeprom") == self.readin_fortests(file)
    
    def test_convert_file_eeprom_2KB(self):
        outfile = "test_output1"
        file = self.inputFiles[1]

        file_dictionary = self.test_ares.split_file([ file ])

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == True
        assert number == 1

        assert self.readin_fortests(f"src/output/{outfile}.eeprom") == self.readin_fortests(file)
    
    def test_convert_file_eeprom_96KB(self):
        outfile = "test_output2"
        file = self.inputFiles[2]

        file_dictionary = self.test_ares.split_file([ file ])

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == True
        assert number == 1

        assert self.readin_fortests(f"src/output/{outfile}.ram") == self.readin_fortests(file)
    
    def test_convert_file_flash(self):
        outfile = "test_output"
        file = self.inputFiles[3]

        file_dictionary = self.test_ares.split_file([ file ])

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == True
        assert number == 1

        assert self.readin_fortests(f"src/output/{outfile}.flash") == self.readin_fortests(file)
    
    def test_convert_file_pak(self):
        outfile = "test_output"
        file = self.inputFiles[4]

        file_dictionary = self.test_ares.split_file([ file ])

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == True
        assert number == 1

        assert self.readin_fortests(f"src/output/{outfile}.pak") == self.readin_fortests(file)
    
    def test_convert_file_ram(self):
        outfile = "test_output"
        file = self.inputFiles[5]

        file_dictionary = self.test_ares.split_file([ file ])

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == True
        assert number == 1

        assert self.readin_fortests(f"src/output/{outfile}.ram") == self.readin_fortests(file)
    
    def test_convert_file_no_files(self):
        outfile = "test_output"
        file_dictionary = {}

        self.test_ares.set_outfile(outfile)

        valid, number = self.test_ares.convert_file(file_dictionary)
        assert valid == False
        assert number == 0

        assert not os.path.exists(f"src/output/{outfile}.eeprom")
        assert not os.path.exists(f"src/output/{outfile}.flash")
        assert not os.path.exists(f"src/output/{outfile}.pak")
        assert not os.path.exists(f"src/output/{outfile}.ram")
    
