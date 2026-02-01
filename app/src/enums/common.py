"""Common enumerations used across the application."""

__all__ = ["Engine", "Mode", "ExceptionType", "Status"]

from enum import Enum


class Engine(str, Enum):
    """Supported data processing engines."""

    duckdb = "duckdb"
    spark = "spark"
    pandas = "pandas"
    pyarrow = "pyarrow"


class Mode(str, Enum):
    """Execution modes for the application."""

    local = "local"
    kubernetes = "kubernetes"


class ExceptionType(str, Enum):
    """Severity levels for exceptions during validations."""

    ignore = "ignore"
    warning = "warning"
    error = "error"


class Status(str, Enum):
    """Status of operations or tasks."""

    success = "success"
    failure = "failure"
    in_progress = "in_progress"
    retry = "retry"
    skipped = "skipped"
