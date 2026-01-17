"""Dataset model for stream-based datasets."""

__all__ = ["StreamDataset"]

from typing import Optional, Dict
from pydantic import Field
from src.models.dataset.base import Dataset


class StreamDataset(Dataset):
    """Dataset model for stream-based datasets."""

    stream_name: str = Field(..., description="The file path of the dataset.")
    file_prefix: Optional[str] = Field(
        None, description="The file prefix of the dataset."
    )
    file_suffix: Optional[str] = Field(
        None, description="The file suffix of the dataset."
    )
    is_partitioned: Optional[bool] = Field(
        False,
        description="Indicates if the dataset is partitioned with subdirectories.",
    )
    args: Optional[Dict] = None
