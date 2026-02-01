"""Model definitions for data sources."""

__all__ = ["SourceConfig"]

from typing import ClassVar, Type, Dict, Any

from pydantic import BaseModel, Field, model_validator

from src.models.common import DummyModel


class SourceConfig(BaseModel):
    """Base model for different types of data sources.
    All sources should accept this config, any additional parameters can be passed via the `args` field.
    """

    name: str = Field(
        ...,
        description="The name of the source, this should match the name in secrets.name",
    )

    args: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional arguments specific to the source type",
    )

    metadata: Dict[str, str] = Field(
        default_factory=dict, description="Optional metadata for the Source"
    )

    # Source/ target can set this args_model so that each source/target can validate the list of args users can set
    # By default no args are expected for all the sources/targets
    args_model: ClassVar[Type[BaseModel]] = DummyModel

    @model_validator(mode="after")
    def validate_args(self):
        """Validate that all mandatory args are present in the args dictionary."""
        self.args = self.args_model.model_validate(self.args)
        return self
