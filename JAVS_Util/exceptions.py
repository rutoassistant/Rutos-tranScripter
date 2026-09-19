"""Custom exception hierarchy for Ruto's tranScripter."""
from __future__ import annotations


class JAVSError(Exception):
    """Base exception for all JAVS errors."""

    staticMessage = "JAVS Error :- "

    def __init__(self, message: str = "Custom JAVS Error") -> None:
        self.message = self.staticMessage + " " + message
        super().__init__(self.message)


class ExtensionError(JAVSError):
    """Raised when a file does not have the .ai extension."""

    def __init__(self) -> None:
        self.message = "Extension Error, Check the Extension as .ai"
        super().__init__(self.message)


class FileNotFountError(JAVSError):
    """Raised when the specified file cannot be found."""

    def __init__(self) -> None:
        self.message = "File Not Found"
        super().__init__(self.message)


class WordNotFound(JAVSError):
    """Raised when a token is not registered in the environment."""

    def __init__(self, Word: str) -> None:
        self.message = f"{Word} Word Not Found In Environment"
        super().__init__(self.message)


class FilePathError(JAVSError):
    """Raised when the file path or name is invalid."""

    def __init__(self) -> None:
        self.message = "Error With the File Path or Name"
        super().__init__(self.message)


class NLTKError(JAVSError):
    """Raised when NLTK fails to download required data."""

    def __init__(self) -> None:
        self.message = "NLTK Module Error, Please Check the internet Connection"
        super().__init__(self.message)


class DotError(JAVSError):
    """Raised when a line is missing the terminating '.' character."""

    def __init__(self, line: int) -> None:
        self.message = f"End of the Line or '.' not Present in the Line - {line}"
        super().__init__(self.message)


class StringNotCompleteError(JAVSError):
    """Raised when a string literal is missing its closing quote."""

    def __init__(self) -> None:
        self.message = "The String that given not complete, ' not found at the end"
        super().__init__(self.message)