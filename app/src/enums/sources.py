from enum import Enum


class SourceType(Enum):
    file = "file"
    database = "database"
    api = "api"
    stream = "stream"
