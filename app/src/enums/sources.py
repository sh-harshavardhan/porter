"""Enumerations related to Sources."""

__all__ = ["SourceType"]


from enum import Enum


class SourceType(Enum):
    """Supported source types for data ingestion."""

    file = "file"
    database = "database"
    api = "api"
    stream = "stream"
