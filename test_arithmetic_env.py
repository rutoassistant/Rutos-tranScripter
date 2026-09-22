"""Tests for ArithmeticEnv operations in Ruto's tranScripter."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from Env.arithmeticEnv import ArithmeticEnv as AE


def test_add() -> None:
    assert AE.addFun("3", "5") == "result =int(3 + 5)"
    assert AE.addFun("$v1", "3") == "result =int(v1 + 3)"


def test_subtract() -> None:
    assert AE.subtractFun("3", "10") == "result =10 - 3"
    assert AE.subtractFun("result", "3") == "result =3 - result"


def test_multiply() -> None:
    assert AE.multiplyFun("4", "5") == "result =4 * 5"


def test_divide() -> None:
    assert AE.divideFun("2", "10") == "result =int(10 / 2)"
    assert AE.divideFun("4", "result") == "result =int(result / 4)"


def test_power() -> None:
    assert AE.powerFun("3", "2") == "result = 2 ** 3"
    assert AE.powerFun("3", "$v1") == "result = v1 ** 3"


def test_modulo() -> None:
    assert AE.moduloFun("3", "10") == "result = 10 % 3"


def test_lt() -> None:
    assert AE.ltFun("3", "5") == "result = 3 < 5"


def test_gt() -> None:
    assert AE.gtFun("5", "3") == "result = 5 > 3"


def test_eq() -> None:
    assert AE.eqFun("4", "4") == "result = 4 == 4"


def test_ne() -> None:
    assert AE.neFun("4", "5") == "result = 4 != 5"


def test_le() -> None:
    assert AE.leFun("3", "5") == "result = 3 <= 5"


def test_ge() -> None:
    assert AE.geFun("5", "3") == "result = 5 >= 3"


def test_increment() -> None:
    assert AE.incrementFun("5") == "result = 5 + 1"


def test_decrement() -> None:
    assert AE.decrementFun("5") == "result = 5 - 1"


def test_env_words_registered() -> None:
    words = AE.env_Words_and_WordAsFunction
    for w in [
        "power",
        "modulo",
        "lt",
        "gt",
        "eq",
        "ne",
        "le",
        "ge",
        "increment",
        "decrement",
    ]:
        assert w in words, f"{w} not registered"


def test_arg_count_validation() -> None:
    for fn in [
        AE.powerFun,
        AE.moduloFun,
        AE.ltFun,
        AE.gtFun,
        AE.eqFun,
        AE.neFun,
        AE.leFun,
        AE.geFun,
    ]:
        try:
            fn("1")
            raise AssertionError(f"{fn.__name__} should reject 1 arg")
        except Exception:
            pass


if __name__ == "__main__":
    import traceback

    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"\u2713 {name}")
            except Exception:
                failures += 1
                print(f"\u2717 {name}")
                traceback.print_exc()
    print(f"\n{failures} failures")
    sys.exit(1 if failures else 0)
