"""Dataset model for Table-based datasets."""

__all__ = ["TableDataset"]

from typing import Optional, Dict
from pydantic import Field
from src.models.dataset.base import Dataset


class TableDataset(Dataset):
    """Dataset model for Table-based datasets."""

    query: str = Field(
        None,
        description="Source query to fetch data from source, which becomes a dataset",
        examples=[
            "SELECT * FROM employees WHERE department = :department",
            "SELECT id, name, sales_amount FROM sales_data_2023 WHERE region = :region",
        ],
    )
    table: Optional[str] = Field(
        None,
        description="Source table name to fetch data from source, which becomes a dataset",
        examples=["employees", "sales_data_2023"],
    )
    values_to_bind: Optional[Dict] = Field(
        None,
        description="If the query has placeholders, this dictionary contains the values to bind to the placeholders",
        examples=[{"department": "Engineering"}, {"region": "North America"}],
    )
    args: Optional[Dict] = Field(
        None,
        description="Additional arguments for fetching the dataset. These are source specific arguments. "
        "Read th documentation for each source to know the list of arguments that it accepts",
    )
