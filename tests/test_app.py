from src.app import add, divide
import pytest

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    try:
        divide(10, 0)
    except ValueError as e:
        assert str(e) == "Tidak boleh bagi nol"
