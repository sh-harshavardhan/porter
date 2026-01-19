"""Dataset model for Table-based datasets."""

__all__ = ["TableDataset"]

from typing import Optional, Dict, List
from pydantic import Field, BaseModel
from src.models.dataset.base import Dataset


class DynamicInputQuery(BaseModel):
    """Model representing a dynamic input query for fetching parameter values."""

    name: str = Field(
        ...,
        description="The name of the dynamic input parameter, this will be used as a placeholder in the main query.",
        examples=["employee_extraction_date", "sales_extraction_date"],
    )
    query: str = Field(
        None,
        description="Query that returns the value for the dynamic input parameter.",
        examples=[
            "SELECT MAX(extraction_date) FROM employees",
            "SELECT MAX(extraction_date) FROM sales_data_2023",
        ],
    )
    source: str = Field(
        ...,
        description="Name of the source on which the dynamic input query has to be executed.",
        examples=["ENV", "hr_database", "sales_database"],
    )


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

    dynamic_input_queries: Optional[List[DynamicInputQuery]] = Field(
        None,
        description="""List of dynamic input query details, each dictionary should contain
        name: The name of the dynamic input parameter, this will be used as a placeholder in the main query.
        query: Query that returns the value for the dynamic input parameter.
        source: Name of the source on which the dynamic input query has to be executed,
                Note : make sure that this source is defined in the pipeline config.""",
        examples=[
            [
                {
                    "name": "employee_extraction_date",
                    "query": "SELECT MAX(extraction_date) FROM employees",
                    "source": "hr_database",
                },
                {
                    "name": "sales_extraction_date",
                    "query": "SELECT MAX(extraction_date) FROM sales_data_2023",
                    "source": "sales_database",
                },
            ]
        ],
    )
