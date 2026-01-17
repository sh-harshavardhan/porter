"""Model definition for Connection Args, which defines the connection parameters for various sources and targets."""

__all__ = ["ConnectionArgs"]


from typing import Optional, Dict, ClassVar, Any
from abc import ABC
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class ConnectionArgs(BaseSettings, ABC):
    """Model representing connection arguments for data sources and targets."""

    HOSTNAME: Optional[str] = None
    PORT: Optional[int] = None
    DATABASE: Optional[str] = None
    USERNAME: Optional[str] = None
    PASSWORD: Optional[str] = None
    DRIVER: Optional[str] = None
    DSN: Optional[str] = None
    CONNECTION_ARGS: Optional[Dict] = None

    # List of mandatory args for each source type.
    # Each Source should define this list based on their requirement,
    # and the validation is done at one place so that not every source have to implement these validations.
    MANDATORY_ARGS: ClassVar[Any] = []

    @classmethod
    def dynamically_subclass_with_prefix(cls, prefix: str):
        """Create a dynamic subclass of the current class with a specific prefix for environment variables."""
        config = {"prefix": prefix, "case_sensitive": False}
        _cls = type(
            cls.__name__, (cls,), {"model_config": SettingsConfigDict(**config)}
        )

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

        if self.secrets and self.secrets_source is None:
            raise ValueError(
                "secrets_source must be provided when secrets are specified"
            )

        return self
