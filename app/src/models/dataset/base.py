"""Base Dataset model for all datasets."""

__all__ = ["Dataset", "Column"]

from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class Column(BaseModel):
    """Model representing a column in a dataset."""

    name: str = Field(..., description="The name of the column")
    target_name: Optional[str] = Field(
        default_factory=lambda data: data.get("name"),
        description="The target name of the column, if not passed will default to the name of the column",
    )
    datatype: Optional[str] = Field(None, description="The datatype of the column")
    precision: Optional[int] = Field(None, description="The precision of the column")
    scale: Optional[int] = Field(None, description="The scale of the column")


class Dataset(BaseModel):
    """Base Dataset model for all datasets."""

    name: str = Field(
        ...,
        description="The name of the dataset",
        examples=["employee_data", "sales_data_2023"],
    )
    columns: List[Column] = Field(
        None,
        description="If you want to specify the schema of the incoming dataset do so "
        "or else it will be inferred for you based on the engine you use."
        "Also remember to use the datatype that the engine you use understands."
        "Example: Use 'str' if you are using pandas, 'STRING' if you are using DuckDB/Spark, etc.",
        examples=[
            {"name": "id", "datatype": "INTEGER"},
            {"name": "name", "datatype": "STRING"},
            {"name": "email", "datatype": "STRING"},
            {"name": "start_date", "datatype": "DATE"},
            {"name": "end_date", "datatype": "DATE"},
            {"name": "department", "datatype": "STRING"},
            {"name": "salary", "datatype": "DECIMAL(20,2)"},
        ],
    )
    metadata: Dict = Field(
        default_factory=lambda data: {"name": data.get("name")},
        description="Metadata for the dataset. By default includes the name of the dataset you dont have to pass it",
        examples=[{"project": "sales_analysis", "owner": "John Doe"}],
    )
