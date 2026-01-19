"""Model related to Porter Config, which defines the overall configuration"""

__all__ = ["PorterConfig"]


from typing import Dict, Optional, Union, List

from pydantic import BaseModel, Field, field_validator
from src.models.dataset import DATASET_TYPES, OnDatasetMissing
from src.models.validation import Validation
from src.models.transform import Transform
from src.models.target import Target
from src.models.source import Source
from src.enums.secrets import SecretSource


class PorterConfig(BaseModel):
    """Model representing the configuration for Porter jobs."""

    name: str = Field(
        ...,
        description="The name of the Porter Config",
    )
    description: Optional[str] = Field(
        None, description="A brief description of the Porter job"
    )

    secrets: Optional[List[str]] = Field(
        default=None,
        description="List of secrets which can be used across sources and targets",
    )
    secrets_source: Optional[str] = Field(
        default=None,
        description="The source from which the secrets are to fetched",
        examples=[ss.name for ss in SecretSource],
    )

    connections: Union[Dict, Source] = Field(
        default=None,
        description="List of all connection details which can be used across sources and targets",
    )

    source: str = Field(
        default=None,
        description="The source name from which data is to be extracted",
    )

    connection_config_paths: str = Field(
        default=None,
        description="Source config path where the source is defined from which data is to be extracted. "
        "Use this if this source is used in multiple Porter jobs. ",
    )

    datasets: Union[DATASET_TYPES] = Field(
        ..., description="List of datasets to be extracted from source"
    )

    on_dataset_missing: Optional[OnDatasetMissing] = Field(
        None,
        description="Action to take when the dataset is missing, this applies to all the datasets. "
        "If the same is defined at dataset level, that will take precedence over this setting.",
    )

    pre_validations: Optional[Validation] = Field(
        None, description="List of validations to be run before the transforms"
    )
    pre_transformations: Optional[Transform] = Field(
        None, description="List of transformations to be run before the main transforms"
    )
    targets: Union[List[Dict], List[Target]] = Field(
        ..., description="List of targets where the data should be loaded"
    )

    post_validations: Optional[Validation] = Field(
        None,
        description="List of validations to be run after the data is loaded into the targets",
    )
    post_transformations: Optional[Transform] = Field(
        None,
        description="List of transformations to be run after the data is loaded into the targets",
    )
    metadata: Optional[Dict] = Field(..., description="Metadata for the Porter job")

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, value):
        """Validate and convert the source field to a Source model if it's provided as a dictionary."""
        if isinstance(value, dict):
            return Source.model_validate(**value)
        return value

    @field_validator("targets", mode="before")
    @classmethod
    def validate_targets(cls, value):
        """Validate and convert the targets field to a list of Target models if provided as a list of dictionaries."""
        if isinstance(value[0], dict):
            return [Target.model_validate(**each_target) for each_target in value]
        return value
