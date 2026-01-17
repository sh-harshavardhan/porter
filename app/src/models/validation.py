"""Model definitions for data Validations."""

__all__ = ["Validation"]


from typing import Dict, Optional
from pydantic import BaseModel, Field
from src.enums.common import ExceptionType


class Validation(BaseModel):
    """Model representing a data validation rule."""

    name: str = Field(..., description="The name of the validation")
    sql_query: str = Field(deafult=None, description="The SQL query for the validation")
    values_to_bind: Optional[Dict] = Field(
        None,
        description="If the query has placeholders, this dictionary contains the values to bind to the placeholders",
    )
    exception: str = Field(
        ..., description="The exception message if the validation fails"
    )
    exception_type: ExceptionType = Field(
        default=ExceptionType.error,
        description="The severity level of the validation failure",
        examples=[exe.value for exe in ExceptionType],
    )
    args: Optional[Dict] = Field(
        default=None, description="Additional arguments for the validation"
    )
    metadata: Optional[Dict] = Field(
        default=None, description="Optional metadata for the validation"
    )
