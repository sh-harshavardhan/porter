"""Enums related to Targets."""

__all__ = ["TargetType", "LoadMode"]


from enum import Enum


class TargetType(str, Enum):
    """Supported target types for data loading."""

    file = "file"
    database = "database"


class LoadMode(str, Enum):
    """Modes for loading data into targets."""

    append = "append"
    overwrite = "overwrite"
    upsert = "upsert"
