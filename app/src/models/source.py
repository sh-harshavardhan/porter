"""Model definitions for data sources."""

__all__ = ["Source"]


from abc import ABC
from typing import Optional, Dict, Any, ClassVar, List
from pydantic import BaseModel, Field, model_validator
from src.enums.secrets import SecretSource


class Source(BaseModel, ABC):
    """Base model for different types of data sources.
    All sources should accept this config, any additional parameters can be passed via the `args` field.
    """

    name: str = Field(..., description="The name of the source")
    secrets: Optional[List[str]] = Field(
        default=None,
        description="List of secrets which contains the credentials for this Source",
    )
    secrets_source: Optional[str] = Field(
        default=None,
        description="The source from which the secrets are to fetched",
        examples=[ss.name for ss in SecretSource],
    )
    args: Any = Field(
        default=None, description="Additional arguments specific to the source type"
    )
    metadata: Optional[Dict] = Field(
        default=None, description="Optional metadata for the source"
    )

    # List of mandatory args for each source type.
    # Each Source should define this list based on their requirement,
    # and the validation is done at one place so that not every source have to implement these validations.
    MANDATORY_ARGS: ClassVar[Any] = []

    @model_validator(mode="after")
    def validate_args(self):
        """Validate that all mandatory args are present in the args dictionary."""
        if self.args is None:
            self.args = {}
        missing_args = [arg for arg in self.MANDATORY_ARGS if arg not in self.args]
        if missing_args:
            raise ValueError(
                f"Missing mandatory args for source type '{self.source_type.name}': {missing_args}"
            )

        if self.secrets and self.secrets_source is None:
            raise ValueError(
                "secrets_source must be provided when secrets are specified"
            )

        return self
