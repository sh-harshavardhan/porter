from enum import Enum


class Engine(Enum):
    duckdb = 'duckdb'
    spark = 'spark'
    pandas = 'pandas'


class Mode(Enum):
    local = 'local'
    kubernetes = 'kubernetes'


class ExceptionTypes(Enum):
    ignore = 'ignore'
    warning = 'warning'
    error = 'error'


class Status(Enum):
    success = 'success'
    failure = 'failure'
    in_progress = 'in_progress'
    retry = 'retry'
    skipped = 'skipped'

