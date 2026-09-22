"""Ruto's tranScripter CLI: natural English → Python transpiler."""
from __future__ import annotations

import os
import sys

from Env.arithmeticEnv import ArithmeticEnv
from JAVS_Util.exceptions import JAVSError
from JAVS_Util.globalTape import JAVGlobalTape
from JAVS_Util.machine import Machine
from JAVS_Util.preCheckFile import PreCheckFile
from JAVS_Util.tokenize import Tokenize


def main(
    path: str, print_log: bool = False, generate_Python_code: bool = False
) -> None:
    try:
        input_string = PreCheckFile.load(path)
        Tokenize.initNLTK()
        tokenize = Tokenize.make(input_string)
        if print_log:
            print("Tokenized Input :- ", tokenize)
        word_list = Tokenize.generateWordListFromEnv(ArithmeticEnv)
        Tokenize.checkAllWordsInEnv(words_list=tokenize, env_words=word_list)
        tape = JAVGlobalTape.make(
            tokenize_input=tokenize, env=ArithmeticEnv, show_logs=print_log
        )
        py_code = Machine.generatePythonCode(tape, ArithmeticEnv)
        if print_log:
            print("Python Code :- ", "\n".join(py_code))

        Machine.executePyCode(py_code)
        if generate_Python_code:
            Machine.generatePyFile(os.path.split(path)[-1][:-3], py_code)
    except JAVSError as jerror:
        print(jerror)
    except Exception as e:
        print("Python Error :- ", e)


def _parse_args(arguments: list[str]) -> tuple[str | None, bool, bool, bool]:
    file_path: str | None = None
    generate_py_code = False
    show_logs = False
    show_env_word = False
    for argument in arguments:
        if argument[0] == "-":
            if "p" in argument:
                generate_py_code = True
            if "l" in argument:
                show_logs = True
            if "envWords" in argument:
                show_env_word = True
        elif ".ai" in argument[-3:]:
            file_path = argument
    return file_path, generate_py_code, show_logs, show_env_word


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        print(
            """Ruto's tranScripter for Achu's Programming Language, a branch which supports Artificial language.
**** Research based project, Not For Production line Product. ****
More documentation https://github.com/rutoassistant/Rutos-tranScripter

.ai file not found.

Command  :-
        javs [file_name.ai] -[flag]

        example :- javs main.ai

        if using python use the command :- python javs.py [file_name.ai] -[flag]

        flag :-
                p := To generate Python code

                l := To generate Log in command Line

                envWords := To get all words in Env
        """
        )

    file_path, generate_py_code, show_logs, show_env_word = _parse_args(arguments)

    if file_path:
        main(file_path, print_log=show_logs, generate_Python_code=generate_py_code)
    elif file_path is None and show_env_word:
        print(f"Env Name :- {ArithmeticEnv.name_of_Env}\n")
        print("Words in the Env :-\n")
        for words in Tokenize.generateWordListFromEnv(ArithmeticEnv):
            print(f"{words}", end="\t")
    else:
        print("JAVS Error :- File Path Not Specified, Or check the Extension")
