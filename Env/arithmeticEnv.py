"""Arithmetic environment: natural language → Python arithmetic expressions."""
from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar

import numpy as np
from numpy.typing import NDArray

from JAVS_Util.globalTape import _EnvBase


class ArithmeticEnv(_EnvBase):
    """Environment that maps natural language words to Python code generators."""

    env_Variables: ClassVar[NDArray[np.str_]] = np.array(["result"])
    name_of_Env: str = "ArithmeticEnv"

    @staticmethod
    def _strip_var(arg: str) -> str:
        """Strip the leading '$' from a variable reference."""
        return arg[1:] if "$" in arg else arg

    @staticmethod
    def addFun(*args: str) -> str:
        parts = [ArithmeticEnv._strip_var(x) for x in args]
        return f"result = int({' + '.join(parts)})"

    @staticmethod
    def multiplyFun(*args: str) -> str:
        parts = [ArithmeticEnv._strip_var(x) for x in args]
        return f"result ={' * '.join(parts)}"

    @staticmethod
    def divideFun(*args: str) -> str:
        parts = [ArithmeticEnv._strip_var(x) for x in reversed(args)]
        return f"result =int({' / '.join(parts)})"

    @staticmethod
    def subtractFun(*args: str) -> str:
        parts = [ArithmeticEnv._strip_var(x) for x in reversed(args)]
        return f"result ={' - '.join(parts)}"

    @staticmethod
    def powerFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("power requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[1])
        b = ArithmeticEnv._strip_var(args[0])
        return f"result = {a} ** {b}"

    @staticmethod
    def moduloFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("modulo requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[1])
        b = ArithmeticEnv._strip_var(args[0])
        return f"result = {a} % {b}"

    @staticmethod
    def ltFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("lt requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[0])
        b = ArithmeticEnv._strip_var(args[1])
        return f"result = {a} < {b}"

    @staticmethod
    def gtFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("gt requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[0])
        b = ArithmeticEnv._strip_var(args[1])
        return f"result = {a} > {b}"

    @staticmethod
    def eqFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("eq requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[0])
        b = ArithmeticEnv._strip_var(args[1])
        return f"result = {a} == {b}"

    @staticmethod
    def neFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("ne requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[0])
        b = ArithmeticEnv._strip_var(args[1])
        return f"result = {a} != {b}"

    @staticmethod
    def leFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("le requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[0])
        b = ArithmeticEnv._strip_var(args[1])
        return f"result = {a} <= {b}"

    @staticmethod
    def geFun(*args: str) -> str:
        if len(args) != 2:
            raise ValueError("ge requires exactly two arguments")
        a = ArithmeticEnv._strip_var(args[0])
        b = ArithmeticEnv._strip_var(args[1])
        return f"result = {a} >= {b}"

    @staticmethod
    def incrementFun(*args: str) -> str:
        if len(args) != 1:
            raise ValueError("increment requires exactly one argument")
        a = ArithmeticEnv._strip_var(args[0])
        return f"result = {a} + 1"

    @staticmethod
    def decrementFun(*args: str) -> str:
        if len(args) != 1:
            raise ValueError("decrement requires exactly one argument")
        a = ArithmeticEnv._strip_var(args[0])
        return f"result = {a} - 1"

    @staticmethod
    def storeFun(*args: str) -> str:
        list_to_print: list[str] = []
        for value in reversed(args):
            if "$" in value:
                if value[1:2] == "~":
                    list_to_print.append(f'"{value[2:]}"')
                else:
                    list_to_print.append(value[1:])
        if len(list_to_print) == 2:
            return f"{list_to_print[1]}={list_to_print[0]}"
        else:
            raise ValueError("Only One variable and one Integer is support")

    @staticmethod
    def theFun(*args: str) -> None:
        return None

    @staticmethod
    def withFun(*args: str) -> None:
        return None

    @staticmethod
    def thenFun(*args: str) -> None:
        return None

    @staticmethod
    def toFun(*args: str) -> None:
        return None

    @staticmethod
    def inFun(*args: str) -> None:
        return None

    @staticmethod
    def andFun(*args: str) -> None:
        return None

    @staticmethod
    def commaFun(*args: str) -> None:
        return ArithmeticEnv.andFun(*args)

    @staticmethod
    def byFun(*args: str) -> None:
        return None

    @staticmethod
    def stringFun(*args: str) -> None:
        return None

    @staticmethod
    def fromFun(*args: str) -> None:
        return None

    @staticmethod
    def printFun(*args: str) -> str:
        list_to_print: list[str] = []
        for value in reversed(args):
            if "$" in value:
                if value[1:2] == "~":
                    list_to_print.append(f'"{value[2:]}"')
                else:
                    list_to_print.append(value[1:])
        return " ".join(["print(", *[f"{x}," for x in list_to_print], ")"])

    @staticmethod
    def displayFun(*args: str) -> str:
        return ArithmeticEnv.printFun(*args)

    env_Words_and_WordAsFunction: ClassVar[dict[str, Callable[..., str | None]]] = {
        "add": addFun,
        "and": andFun,
        ",": commaFun,
        "print": printFun,
        "multiply": multiplyFun,
        "store": storeFun,
        "to": toFun,
        "in": inFun,
        "divide": divideFun,
        "by": byFun,
        "display": displayFun,
        "the": theFun,
        "then": thenFun,
        "with": withFun,
        "string": stringFun,
        "subtract": subtractFun,
        "from": fromFun,
        "power": powerFun,
        "modulo": moduloFun,
        "lt": ltFun,
        "gt": gtFun,
        "eq": eqFun,
        "ne": neFun,
        "le": leFun,
        "ge": geFun,
        "increment": incrementFun,
        "decrement": decrementFun,
    }
