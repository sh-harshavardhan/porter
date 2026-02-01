"""Model definition for Database Args, which defines the connection parameters for various sources and targets."""

__all__ = ["DBArgs"]


from typing import Optional, Dict
from pydantic import BaseModel


class DBArgs(BaseModel):
    """Model representing connection arguments for data sources and targets."""

    HOSTNAME: Optional[str] = None
    PORT: Optional[int] = None
    DATABASE: Optional[str] = None
    USERNAME: Optional[str] = None
    PASSWORD: Optional[str] = None
    DRIVER: Optional[str] = None
    DSN: Optional[str] = None
    CONNECTION_ARGS: Optional[Dict] = None
