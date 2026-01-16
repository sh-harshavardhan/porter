from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class Column(BaseModel):
    name: str = Field(
        ...,
        description="The name of the column"
    )
    target_name: Optional[str] = Field(
        default_factory=lambda data: data.get('name'),
        description="The target name of the column, if not passed will default to the name of the column"
    )
    datatype: Optional[str] = Field(
        None,
        description="The datatype of the column"
    )
    precision: Optional[int] = Field(
        None,
        description="The precision of the column"
    )
    scale: Optional[int] = Field(
        None,
        description="The scale of the column"
    )


class Dataset(BaseModel):
    name: str = Field(
        ...,
        description="The name of the dataset"
    )
    columns: List[Column] = Field(
        None,
        description="The List of columns in the dataset."
    )
    metadata: Optional[Dict] = Field(
        None,
        description="Optional metadata for the dataset"
    )

