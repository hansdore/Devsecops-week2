# src/app.py

import shlex
import subprocess

def add(a, b):
    """Menambahkan dua angka."""
    return a + b

def divide(a, b):
    """Membagi dua angka dengan pengecekan pembagi nol."""
    if b == 0:
        raise ValueError("Tidak boleh bagi nol")
    return a / b

def run_command(cmd):
    """
    Menjalankan perintah shell dengan aman.
    - Tidak menggunakan shell=True (mencegah injection).
    - Jika cmd berupa string, gunakan shlex.split() untuk parsing.
    - Mengembalikan output perintah atau pesan error.
    """
    if isinstance(cmd, str):
        args = shlex.split(cmd)
    elif isinstance(cmd, (list, tuple)):
        args = list(cmd)
    else:
        raise TypeError("cmd harus berupa string, list, atau tuple")

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Perintah gagal: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Perintah tidak ditemukan"
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# Contoh pemanggilan manual (tidak akan jalan di pipeline CI)
if __name__ == "__main__":
    print("Hasil tambah:", add(3, 5))
    print("Hasil bagi:", divide(10, 2))
    print("Coba perintah:", run_command("echo Hello World"))
