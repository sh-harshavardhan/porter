"""Dataset model for file-based datasets."""

__all__ = ["FileDataset"]

from typing import Optional
from pydantic import Field
from src.models.dataset.base import Dataset
from src.enums import datasets, common


class FileDataset(Dataset):
    """Dataset model for file-based datasets.
    Files in the path matching the prefix and suffix will be included in the dataset.
    Example: /path/to/data/prefix_*.csv
    """

    file_path: str = Field(..., description="The file path of the dataset.")
    file_type: datasets.FileTypes = Field(
        ...,
        description="Type of the file.",
        examples=[f.name for f in datasets.FileTypes],
    )
    engine: common.Engine = Field(
        common.Engine.pandas,
        description="Which Engine to use to read the file, By default PANDAS is used",
        examples=[e.name for e in common.Engine],
    )
    file_pattern: Optional[str] = Field(
        default="*",
        description="""The file pattern, Uses glob patterning.
                    By default all the files under `file_path` will be processed.
                    Also if either `file_prefix` or `file_suffix` they take precedence.
                    """,
        examples=["DB_FILE_*.csv", "sales_data_*.json", "EMP_REC_*_PART_*_.parquet"],
    )
    file_prefix: Optional[str] = Field(
        None,
        description="The file prefix of the dataset, use this if the source cannot handle glob patterns.",
        examples=["/source_data/DB_FILE_", "sales_data_", "EMP_REC_"],
    )
    file_suffix: Optional[str] = Field(
        None,
        description="The file suffix of the dataset, this will be added at the end of the file pattern. "
        "Use this if the source cannot handle glob patterns.",
        examples=[".csv", ".json", ".parquet"],
    )
    is_partitioned: Optional[bool] = Field(
        False,
        description="Indicates if the dataset is partitioned with subdirectories.",
    )
