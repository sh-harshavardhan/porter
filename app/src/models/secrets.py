"""Model definitions for SecretsBackend."""

__all__ = ["SecretsBackend"]


from abc import ABC
from typing import Optional, Dict, Type, ClassVar, List, Any
from pydantic import BaseModel, Field, model_validator
from src.enums.secrets import SecretSource
from src.models.common import DummyModel


class SecretsBackend(BaseModel, ABC):
    """Model representing SecretsBackend config file which allows us to define the secrets backend source."""

    name: str = Field(..., description="The name of the source")
    secrets: Optional[List[str]] = Field(
        default=None,
        description="List of secrets which contains the credentials for Sources/Targets"
        "Only Secrets mentioned here will be allowed in Porter jobs."
        "Leave this empty to allow all secrets from the Secrets source.",
        examples=[
            """
            - /dev/oracle/sales
            - /dev/oracle/hr
            - /dev/oracle/finance
            """
        ],
    )
    secrets_source: SecretSource = Field(
        ...,
        description="The Secrets source from which the secrets are to fetched",
        examples=[ss.name for ss in SecretSource],
    )
    args: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional arguments specific to the source type",
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict, description="Optional metadata for the Secrets Backend"
    )

    # Secrets Backend can set this args_model so that each Secrets Backend can validate the list of args users can set
    # By default no args are expected for all the Secrets Backend
    args_model: ClassVar[Type[BaseModel]] = DummyModel

    @model_validator(mode="after")
    def validate_args(self):
        """Validate that all mandatory args are present in the args dictionary."""
        self.args = self.args_model.model_validate(self.args)
        return self
