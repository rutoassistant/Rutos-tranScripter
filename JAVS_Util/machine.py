"""Machine: generates and executes Python code from the global tape."""
from __future__ import annotations

import numpy as np

from JAVS_Util.globalTape import _EnvBase


class Machine:
    """Translates a list of sentence tapes into executable Python code."""

    @staticmethod
    def generatePythonCode(global_tape: np.ndarray, env: type[_EnvBase] | _EnvBase) -> list[str]:
        python_code: list[str] = []
        for sentence_tape in global_tape:
            variable_buffer: list[str] = []
            python_code_sentence: list[str] = []
            for word in reversed(sentence_tape):
                if "$" in word:
                    variable_buffer.append(word)
                else:
                    result = env.env_Words_and_WordAsFunction[str(word).lower()](
                        *variable_buffer
                    )
                    if result is not None:
                        python_code_sentence = [result, *python_code_sentence]
                        variable_buffer = []
            python_code = [*python_code, *python_code_sentence]
        return python_code

    @staticmethod
    def executePyCode(code: list[str]) -> None:
        exec("\n".join(code))

    @staticmethod
    def generatePyFile(filename: str, code: list[str]) -> None:
        with open(file=f"{filename}.generated.py", mode="w") as f:
            f.writelines("\n".join(code))
            print("**** Python Code Generated ****")
