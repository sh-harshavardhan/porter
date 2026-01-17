from typing import Optional, Dict

from src.models.dataset.base import Dataset, Field


class TableDataset(Dataset):
    """
    Dataset model for Table-based datasets.
    """

    query: str = Field(
        None,
        description="Source query to fetch data from source, which becomes a dataset",
    )
    table: Optional[str] = Field(
        None,
        description="Source table name to fetch data from source, which becomes a dataset",
    )
    values_to_bind: Optional[Dict] = Field(
        None,
        description="If the query has placeholders, this dictionary contains the values to bind to the placeholders",
    )
    args: Optional[Dict] = None
