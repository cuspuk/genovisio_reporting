# custom exception classes
class GenovisioReportError(Exception):
    """Base class for exceptions in this module."""

    pass


class InputFileInvalidError(GenovisioReportError):
    """Exception raised when an input file is invalid."""

    def __init__(self, input_file: str, valid_extensions: list[str]):
        message = f"Invalid extension of {input_file=}. See {valid_extensions=}"
        super().__init__(message)
