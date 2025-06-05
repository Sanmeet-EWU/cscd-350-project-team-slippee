import os
from emulators import bizhawk

base_dir = os.getcwd()
if os.path.basename(base_dir) == "src":
    base_dir = os.path.dirname(base_dir)

output_dir = os.path.join(base_dir, "src", "output")
os.makedirs(output_dir, exist_ok=True)


def readin(file: str) -> bytes:
    '''
    Reads in the bytes from the given file

    '''
    try:
        with open(file, "rb") as inp:
            return inp.read()
    except FileNotFoundError:
        print("File Does Not Exist")
        return b""
    except Exception as e:
        print(f"Exception Occurred:\n{e}")
        return b""

def writeout(name: str, file: bytes) -> None:
    '''
    Writes the given bytes to the given file

    name
        the name of the file to write to

    file
        the bytes to write to the file
    '''
    full_path = os.path.join(output_dir, name)

    with open(full_path, "wb") as out:
        out.write(file)

def clone_template(name: str) -> None:
    '''
    Clones the template file to the given name
    
    name
        the name of the file to clone to
    '''
    full_path = os.path.join(output_dir, name)

    with open("src/template/temp", "rb") as inp:
        with open(full_path, "wb") as out:
            out.write(inp.read())
            return True