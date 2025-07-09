from functions.run_python_file import run_python_file

def test():
    print("1.")
    print(run_python_file("calculator", "main.py"))
    print("2.")
    print(run_python_file("calculator", "tests.py"))    
    print("3.")
    print(run_python_file("calculator", "../main.py"))
    print("4.")
    print(run_python_file("calculator", "nonexistent.py"))
    
if __name__ == "__main__":
    test()

