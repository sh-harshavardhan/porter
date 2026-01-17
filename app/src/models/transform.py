"""Model definitions for data Transformations."""

__all__ = ["Transform"]


from typing import Optional, Dict
from pydantic import BaseModel, Field


class Transform(BaseModel):
    """Model representing a data transformation rule."""

    name: str = Field(..., description="The name of the transform")
    source_name: str = Field(
        default="duck_internal",
        description="The name of the source in which the transform has to be ran. "
        "Defaults to 'duck_internal', which is created by default at the start of every job."
        "And also contains all the datasets created during the job execution.",
    )
    sql_query: Optional[str] = Field(
        None, description="The SQL query for the transform"
    )
    sql_path: Optional[str] = Field(
        None, description="The file path containing the SQL query for the transform"
    )
    values_to_bind: Optional[Dict] = Field(
        None,
        description="If the query has placeholders, this dictionary contains the values to bind to the placeholders",
    )
