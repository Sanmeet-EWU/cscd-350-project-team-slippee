from abc import ABC, abstractmethod

# Abstract parent class
class Emulator(ABC):
    inputFile = []
    outfile = ""

    # To be defined in child classes
    @abstractmethod
    def convert_file(self, inputFiles: dict) -> bool: 
        '''
        abstract method to be defined in child classes
        
        converts files to the correct syntax for the emulator

        inputFiles
            a dictionary of all the save types

        returns a boolean indicating whether the conversion was successful
        '''
        pass

    @abstractmethod
    def split_file(self, file: list) -> dict:
        '''
        abstract method to be defined in child classes

        splits each file in the given list based on defined parameters

        file
            list of files to split

        returns a dictionary containing each files bytestreams  
        with name as key
        '''
        pass
    
    def set_outfile(self, inp: str) -> bool:
        '''
        Sets the outfile string

        Returns the status of whether outfile was set

        inp
            the input file name
        '''
        if isinstance(inp, str): # Making sure the input is a string
            self.outfile = inp
            return True
        
        return False

    def get_outfile(self) -> str:
        '''
        getter for outfile

        Returns the output file 
        '''
        return self.outfile
    
    def get_input_file(self) -> list:
       '''
       getter for inputFile
       
       Returns the inputFile list
       '''
       return self.inputFile

    # setter for inputFile
    def set_input_file(self, inFiles: list) -> bool:
        '''
        Sets the inputFile list to the given list

        Returns the status whether the list was set

        inFiles
            a list containing all files to parse
        '''
        if isinstance(inFiles, list):
            self.inputFile = inFiles
            return True
        return False

    # Convert from little endian to big endian, and visa versa
    def endian_fix(self, inString: bytes) -> bytes:
        '''
        Switches endianess of the input bytestream

        EmuHawk switches the endianness fo some files  
        so this fixes that.

        Returns the bytestream with it's endianness swapped
        '''
        # Ensures the size is divisible by 4
        if not len(inString) % 4 == 0: 
            return b""
        
        if not isinstance(inString, bytes):
            return b""
        
        temp = b""
        for i in range(len(inString) // 4):
            # Inverts every group of 4 bytes and appends
            temp += inString[i * 4: (i + 1) * 4][::-1] 
        
        return temp

