"""Model related to Porter Pipeline Config, which defines the overall configuration"""

__all__ = ["PorterPipeline"]


from typing import Dict, Optional, Union, List

from pydantic import BaseModel, Field, FilePath, field_validator, model_validator
from src.models.dataset import (
    OnDatasetMissing,
    Dataset,
    ApiDataset,
    TableDataset,
    FileDataset,
)
from src.models.validation import ValidationConfig
from src.models.transform import TransformConfig
from src.models.target import TargetConfig
from src.models.source import SourceConfig
from src.models.secrets import SecretsBackend


class PorterPipeline(BaseModel):
    """Model representing the configuration for Porter pipeline."""

    name: str = Field(
        ...,
        description="The name of the Porter pipeline",
    )

    description: Optional[str] = Field(
        None, description="A brief description of the Porter job"
    )

    source: Union[Dict, SourceConfig] = Field(
        default=None,
        description="The source name from which data is to be extracted",
    )

    secrets_backend: Union[Dict, SecretsBackend] = Field(
        default=None,
        description="The secrets backend to be used for fetching secrets ",
    )

    secrets_backend_config: Optional[FilePath] = Field(
        default=None,
        description="The secrets backend config name to be used for fetching secrets ",
    )

    datasets: List[Union[Dataset, ApiDataset, TableDataset, FileDataset]] = Field(
        ..., description="List of datasets to be extracted from source"
    )

    on_dataset_missing: Optional[OnDatasetMissing] = Field(
        None,
        description="Action to take when the dataset is missing, this applies to all the datasets. "
        "If the same is defined at dataset level, that will take precedence over this setting.",
    )

    pre_validations: Optional[ValidationConfig] = Field(
        None, description="List of validations to be run before the transforms"
    )
    pre_transformations: Optional[TransformConfig] = Field(
        None, description="List of transformations to be run before the main transforms"
    )
    targets: Union[List[Dict], List[TargetConfig]] = Field(
        ..., description="List of targets where the data should be loaded"
    )

    post_validations: Optional[ValidationConfig] = Field(
        None,
        description="List of validations to be run after the data is loaded into the targets",
    )
    post_transformations: Optional[TransformConfig] = Field(
        None,
        description="List of transformations to be run after the data is loaded into the targets",
    )
    metadata: Optional[Dict] = Field(..., description="Metadata for the Porter job")

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, value):
        """Validate and convert the source field to a Source model if it's provided as a dictionary."""
        if isinstance(value, dict):
            return SourceConfig.model_validate(value)
        return value

    @field_validator("targets", mode="before")
    @classmethod
    def validate_targets(cls, value):
        """Validate and convert the targets field to a list of Target models if provided as a list of dictionaries."""
        if isinstance(value[0], dict):
            return [TargetConfig.model_validate(each_target) for each_target in value]
        return value

    @field_validator("secrets_backend", mode="before")
    @classmethod
    def validate_secrets_backend(cls, value):
        """Validate secrets_backend field to convert to SecretsBackend model if provided as a dictionary."""
        if isinstance(value, Dict):
            return SecretsBackend.model_validate(value)
        return value

    @model_validator(mode="after")
    def read_secrets_backend_config(self):
        """Read the secrets backend config file if provided and set it to the secrets_backend field"""
        if self.secrets_backend_config and self.secrets_backend is None:
            from src.common.config import read_config_file

            self.secrets_backend = read_config_file(
                self.secrets_backend_config, SecretsBackend
            )
        return self
