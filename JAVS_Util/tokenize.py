"""Natural language tokenization backed by NLTK."""
from __future__ import annotations

import nltk
import numpy as np
from numpy.typing import NDArray

from .exceptions import NLTKError, WordNotFound


class Tokenize:
    """Tokenizes natural language input into numpy arrays of strings."""

    @staticmethod
    def initNLTK() -> None:
        try:
            nltk.data.find("tokenizers/punkt")
        except Exception:
            if not nltk.download("punkt", quiet=True):
                raise NLTKError()

    @staticmethod
    def make(input_string: str) -> NDArray[np.str_]:
        return np.array(nltk.word_tokenize(str(input_string)))

    @staticmethod
    def checkAllWordsInEnv(
        words_list: NDArray[np.str_], env_words: list[str]
    ) -> None:
        string_variable_flag = False
        variable_flag = False
        for word in words_list:
            if "'" in word:
                string_variable_flag = not string_variable_flag
            elif "$" in word:
                variable_flag = True
            elif variable_flag:
                variable_flag = False
            elif (
                str(word).lower() not in env_words
                and not str(word).isnumeric()
                and "." not in word
                and not string_variable_flag
            ):
                raise WordNotFound(Word=str(word))

    @staticmethod
    def generateWordListFromEnv(env: object) -> list[str]:
        env_vars: list[str] = list(env.env_Variables)  # type: ignore[attr-defined]
        env_keys: list[str] = list(env.env_Words_and_WordAsFunction.keys())  # type: ignore[attr-defined]
        return env_vars + env_keys