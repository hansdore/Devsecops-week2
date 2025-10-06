# src/app.py

import shlex
import subprocess

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Tidak boleh bagi nol")
    return a / b

def run_command(cmd):
    """
    FIX: Jangan gunakan shell=True.
    - Jika cmd adalah string: gunakan shlex.split(cmd) -> list of args
    - Atau, panggil subprocess.run dengan list args
    """
    # Jika caller mengirim string, split aman jadi list
    if isinstance(cmd, str):
        args = shlex.split(cmd)
    else:
        # anggap cmd sudah list/tuple
        args = cmd

    # Tidak ada shell=True -> menghindari command injection
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout

