"""Model definitions for data sources which can be Targets."""

__all__ = ["Target"]


from abc import ABC
from typing import List, Optional, Dict, ClassVar, Any

from pydantic import Field, BaseModel, model_validator

from src.enums.targets import LoadMode


class CustomWriteOptions(BaseModel):
    """Model representing custom write options for a specific target and dataset."""

    dataset_name: str = Field(
        ...,
        description="The name of the dataset for which the custom option is applied",
    )
    target_name: Optional[str] = Field(
        default_factory=lambda data: data.get("dataset_name"),
        description="The target name of the dataset, if different from the original name",
    )
    truncate_target: bool = Field(
        default=False,
        description="Flag indicating whether to truncate the target dataset before loading",
    )
    mode: Optional[LoadMode] = Field(
        default=LoadMode.append,
        description="The load mode for this specific dataset",
        examples=[mode.name for mode in LoadMode],
    )


class Target(BaseModel, ABC):
    """Model representing a data target, inheriting from Source."""

    name: str = Field(..., description="The name of the target")

    metadata: Optional[Dict] = Field(
        None, description="Optional metadata for the source"
    )

    mode: LoadMode = Field(
        default=LoadMode.append,
        description="The load mode for the target",
        examples=[mode.name for mode in LoadMode],
    )

    load_all: bool = Field(
        default=True,
        description="Flag indicating whether to load all dataset into the target",
    )
    load_only: Optional[List] = Field(
        default=None,
        description="List of specific datasets to load into the target. If not set, all datasets will be loaded.",
    )
    rename_targets: Optional[Dict[str, str]] = Field(
        default=None,
        description="Dictionary to rename datasets when loading into the target. "
        "Keys are original dataset names, values are new target names.",
    )
    truncate_before_load: bool = Field(
        default=False,
        description="Flag indicating whether to truncate existing data in the target before loading new data",
    )

    custom_write_options: Optional[List[CustomWriteOptions]] = Field(
        default=None,
        description="List of custom options for the target load operation",
        examples=[
            [
                {
                    "dataset_name": "sales_data",
                    "target_name": "sales_2023",
                }
            ],
            [
                {
                    "dataset_name": "customers",
                    "target_name": "customers_current",
                    "truncate_target": True,
                }
            ],
        ],
    )

    # List of mandatory args for each source type.
    # Each Source should define this list based on their requirement,
    # and the validation is done at one place so that not every source have to implement these validations.
    MANDATORY_ARGS: ClassVar[Any] = []

    @model_validator(mode="after")
    def validate_args(self):
        """Validate that all mandatory arguments are present."""
        if self.args is None:
            self.args = {}
        missing_args = [arg for arg in self.MANDATORY_ARGS if arg not in self.args]
        if missing_args:
            raise ValueError(
                f"Missing mandatory args for source type '{self.source_type.name}': {missing_args}"
            )

        return self
