"""Enums related to Targets."""

__all__ = ["TargetType", "LoadMode"]


from enum import Enum


class TargetType(Enum):
    """Supported target types for data loading."""

    file = "file"
    database = "database"


class LoadMode(Enum):
    """Modes for loading data into targets."""

    append = "append"
    overwrite = "overwrite"
    upsert = "upsert"
