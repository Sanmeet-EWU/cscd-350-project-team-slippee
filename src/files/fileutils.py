import os

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
    os.makedirs("output", exist_ok=True)
    with open(f"output/{name}", "wb") as out:
        out.write(file)

def clone_template(name: str) -> None:
    os.makedirs("output", exist_ok=True)
    with open("template/temp", "rb") as inp:
            with open(f"output/{name}", "wb") as out:
                out.write(inp.read())
                return True
            