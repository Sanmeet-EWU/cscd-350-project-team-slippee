
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
    with open(f"src/output/{name}", "wb") as out:
        out.write(file)

def clone_template(name: str) -> None:
    with open("src/template/temp", "rb") as inp:
            with open(f"src/output/{name}", "wb") as out:
                out.write(inp.read())
                return True
            