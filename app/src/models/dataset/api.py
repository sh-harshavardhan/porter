"""Dataset model for api-based datasets."""

__all__ = ["ApiDataset"]

from typing import Optional, Dict
from pydantic import Field
from src.models.dataset.base import Dataset


class ApiDataset(Dataset):
    """Dataset model for api-based datasets."""

    url: str = Field(
        None,
        description="API endpoint to fetch data from source, which becomes a dataset",
    )
    auth_url: Optional[str] = Field(
        None, description="Authentication URL to get access token if required"
    )
    args: Optional[Dict] = None
