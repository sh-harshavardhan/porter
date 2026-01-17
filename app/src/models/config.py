"""Model related to Porter Config, which defines the overall configuration"""

__all__ = ["PorterConfig"]


from typing import Dict, Optional, Union, List

from pydantic import BaseModel, Field, field_validator
from src.models.dataset import DATASET_TYPES
from src.models.validation import Validation
from src.models.transform import Transform
from src.models.target import Target, CustomWriteOptions
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

    source: Union[Dict, Source] = Field(
        default=None,
        description="The source details from which data is to be extracted",
    )

    source_config_path: str = Field(
        default=None,
        description="Source config path where the source is defined from which data is to be extracted. "
        "Use this if this source is used in multiple Porter jobs. ",
    )

    datasets: Union[DATASET_TYPES] = Field(
        ..., description="List of datasets to be extracted from source"
    )
    pre_validations: Optional[Validation] = Field(
        None, description="List of validations to be run before the transforms"
    )
    pre_transformations: Optional[Transform] = Field(
        None, description="List of transformations to be run before the main transforms"
    )
    # Targets can be passed as list of dicts or list of Target objects.
    # In case of YAML config these will be read as dict and validated against Target model.
    targets: Union[List[Dict], List[Target]] = Field(
        ..., description="List of targets where the data should be loaded"
    )

    custom_write_options: Optional[List[CustomWriteOptions]] = Field(
        default=None,
        description="List of custom options for the target load operation",
        examples=[
            [
                {
                    "target": "postgres",
                    "dataset_name": "sales_data",
                    "target_name": "sales_2023",
                }
            ],
            [
                {
                    "target": "s3",
                    "dataset_name": "customers",
                    "target_name": "customers_current",
                    "truncate_target": True,
                }
            ],
        ],
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
