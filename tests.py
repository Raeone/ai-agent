import main
import subprocess
from call_function import call_function

def test():
    arg = ''
    result = subprocess.run(
        ["python3", "main.py", "what is content of calculator directory?" "--verbose"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    
if __name__ == "__main__":
    test()
