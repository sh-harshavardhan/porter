from typing import Optional, Dict

from src.models.dataset.base import Dataset, Field


class FileDataset(Dataset):
    """
    Dataset model for file-based datasets.
    Files in the path matching the prefix and suffix will be included in the dataset.
    Example: /path/to/data/prefix_*.csv
    """

    file_path: str = Field(..., description="The file path of the dataset.")
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
