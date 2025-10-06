def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Tidak boleh bagi nol")
    return a / b
import subprocess

def run_command(cmd):
    # BUG: penggunaan shell=True berbahaya (Command Injection)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout
