from enum import Enum


class TargetType(Enum):
    file = 'file'
    database = 'database'


class LoadMode(Enum):
    append = 'append'
    overwrite = 'overwrite'
    upsert = 'upsert'
