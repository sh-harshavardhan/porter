from src.models.dataset.base import Dataset
from src.models.dataset.api import ApiDataset
from src.models.dataset.table import TableDataset
from src.models.dataset.file import FileDataset


DATASET_TYPES = [Dataset, ApiDataset, TableDataset, FileDataset]
