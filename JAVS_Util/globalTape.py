"""Global tape construction from tokenized input using numpy arrays."""
from __future__ import annotations

from typing import Any, Optional

import numpy as np
from numpy.typing import NDArray

from .rightHandTree import RightHandTree


class JAVGlobalTape:
    """Builds a list of sentence tapes from a numpy array of tokens."""

    @staticmethod
    def make(
        tokenize_input: NDArray[np.str_],
        env: Any,
        show_logs: bool = False,
    ) -> list[list[str]]:
        string_initial_constant = "$~"
        global_tape: list[list[str]] = []
        iterate_each_word = iter(tokenize_input)
        catch_variable_value = False
        end_of_a_sentence = True
        node: Optional[RightHandTree] = None
        catch_string_variable = False
        string_variable = f"{string_initial_constant}"
        try:
            while True:
                current_word = next(iterate_each_word)
                if "$" == current_word and not catch_variable_value and not catch_string_variable:
                    catch_variable_value = True
                elif "'" in current_word:
                    if current_word == "'":
                        catch_string_variable = not catch_string_variable
                        if not catch_string_variable:
                            current_word = string_variable
                            string_variable = f"{string_initial_constant}"
                            if node is not None:
                                node.insertNode(current_word)
                    else:
                        catch_string_variable = not catch_string_variable
                        string_variable = f"{string_initial_constant}{current_word[1:]}"
                elif catch_string_variable:
                    if len(str(string_variable)) == 2:
                        string_variable = f"{string_variable}{current_word}"
                    else:
                        string_variable = f"{string_variable} {current_word}"
                elif "." == current_word and not end_of_a_sentence:
                    end_of_a_sentence = True
                    if show_logs:
                        print("\nCustom Tree Structure of the current Sentence :- \n")
                    if show_logs and node is not None:
                        node.PrintTree()
                    tape = node.makeTape() if node is not None else []
                    global_tape.append(tape)
                    if show_logs:
                        print("\nEnd of a sentence", "\nTape :- \n", tape, "\n")
                else:
                    if end_of_a_sentence:
                        if show_logs:
                            print("\nStarting of a sentence\n")
                        end_of_a_sentence = False
                        node = RightHandTree()
                    if catch_variable_value:
                        catch_variable_value = False
                        current_word = "$" + current_word
                    elif str(current_word).isnumeric():
                        current_word = "$" + current_word
                    elif current_word in env.env_Variables:
                        current_word = "$" + current_word
                    if node is not None:
                        node.insertNode(current_word)
        except StopIteration:
            if show_logs:
                print("\nEnd of All the lines\n")
                print("\nGlobal Tape:-\n", global_tape)
        return global_tape