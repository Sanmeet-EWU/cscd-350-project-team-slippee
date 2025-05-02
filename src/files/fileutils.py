

def readin(file):
    try:
        with open(file, "rb") as inp:
            return inp.read()
    except FileNotFoundError:
        print("File Does Not Exist")
    except Exception as e:
        print(f"Exception Occurred:\n{e}")