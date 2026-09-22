"""File pre-checking utilities for Ruto's tranScripter."""
from __future__ import annotations

from .exceptions import DotError, ExtensionError, FileNotFountError


class PreCheckFile:
    """Validates and loads .ai source files."""

    @staticmethod
    def load(file_path: str) -> str:
        if not isinstance(file_path, str):
            raise FileNotFountError()
        if ".ai" not in file_path:
            raise ExtensionError()
        try:
            with open(file_path) as file:
                final_string: list[str] = []
                for index, line in enumerate(file.readlines()):
                    if line != "\n":
                        if "." in str(line).replace("\n", "")[-2:]:
                            final_string.append(line)
                        else:
                            raise DotError(index + 1)
                return "".join(final_string)
        except Exception as e:
            raise e
