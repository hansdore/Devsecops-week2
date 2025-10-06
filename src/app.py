# src/app.py

"""
Safe utilities for demo DevSecOps project.

Fitur:
- add(a, b) -> penjumlahan sederhana
- divide(a, b) -> pembagian dengan pengecekan pembagi nol
- run_command(cmd, timeout=10) -> menjalankan command secara aman tanpa shell=True
  - menerima `cmd` sebagai list/tuple of args atau string (akan di-split dengan shlex)
  - menghindari penggunaan shell=True untuk mencegah command injection
  - mengembalikan dict {'stdout': str, 'stderr': str, 'returncode': int}
"""

from __future__ import annotations
import shlex
import subprocess
from typing import Union, List, Dict


def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


def divide(a: float, b: float) -> float:
    """
    Return a / b. Raises ValueError when dividing by zero.
    """
    if b == 0:
        raise ValueError("Tidak boleh bagi nol")
    return a / b


def run_command(cmd: Union[str, List[str], tuple], timeout: int = 10) -> Dict[str, Union[str, int]]:
    """
    Execute a command safely without using shell=True.

    Args:
        cmd: Command to run. Bisa berupa:
             - list/tuple: ['ls', '-la']
             - string: "ls -la" (akan di-split menggunakan shlex.split)
        timeout: Timeout dalam detik (default 10). Jika command melebihi timeout, subprocess.TimeoutExpired di-handle.

    Returns:
        dict: {'stdout': <str>, 'stderr': <str>, 'returncode': <int>}

    Raises:
        ValueError: jika cmd kosong atau bukan tipe yang diharapkan.
    """
    if not cmd:
        raise ValueError("cmd tidak boleh kosong")

    # Normalisasi argumen menjadi list
    if isinstance(cmd, str):
        # shlex.split aman untuk memisahkan string menjadi list argumen
        args = shlex.split(cmd)
    elif isinstance(cmd, (list, tuple)):
        args = list(cmd)
    else:
        raise ValueError("cmd harus str, list, atau tuple")

    # Pastikan ada minimal satu argumen
    if len(args) == 0:
        raise ValueError("cmd harus berisi nama program/command")

    try:
        # Tidak menggunakan shell=True — menggunakan list args lebih aman
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False  # jangan raise CalledProcessError otomatis
        )
    except subprocess.TimeoutExpired as ex:
        # Jika timeout, kembalikan informasi yang berguna
        return {
            "stdout": ex.stdout or "",
            "stderr": (ex.stderr or "") + f"\nCommand timed out after {timeout} seconds",
            "returncode": -1
        }
    except Exception as ex:
        # Penangkap error umum (mis. FileNotFoundError ketika command tidak ada)
        return {
            "stdout": "",
            "stderr": str(ex),
            "returncode": -1
        }

    return {
        "stdout": completed.stdout or "",
        "stderr": completed.stderr or "",
        "returncode": completed.returncode
    }

