"""Enumerations related to Datasets."""

__all__ = ["FileTypes", "OnDatasetMissingActions"]

from enum import Enum


class FileTypes(str, Enum):
    """Supported file types for datasets."""

    csv = "csv"
    json = "json"
    parquet = "parquet"
    excel = "excel"
    xml = "xml"
    fixed_width = "fixed_width"
    avro = "avro"
    orc = "orc"
    custom = "custom"


class OnDatasetMissingActions(str, Enum):
    """Supported actions when a dataset is missing."""

    error = "error"
    warning = "warning"
    poll = "poll"
