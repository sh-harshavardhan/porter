"""Base class for all data sources. Defines what methods need to be implemented by each source.
Also lets each source define if it can be used as a source or target or both.
"""

__all__ = ["Source"]

from abc import ABC, abstractmethod
from src.models.source import SourceConfig


class Source(ABC):
    """This is a base class for all the sources/ All sources must implement the methods defined here.
    This class also allows each source to define if it can be a source or a target or both.
    """

    def __init__(self, config: SourceConfig):
        """Expect to pass source config to all sources"""
        self.config = config

    @property
    @abstractmethod
    def is_source(self):
        """Indicate True if the source can be used as a Source, by default is False"""
        ...

    @property
    @abstractmethod
    def is_target(self):
        """Indicate True if the source can be used as a Target, by default is False"""
        ...

    def read(self, **kwargs):
        """Method to read data from the source"""
        if self.is_source():
            raise NotImplementedError("Read method not implemented for this source")

    def write(self, **kwargs):
        """Method to write data to the target"""
        if self.is_target():
            raise NotImplementedError("Write method not implemented for this source")

    def execute(self, **kwargs):
        """This method doesn't have be implemented by all sources.
        Implement this method if you want to execute something on a source like SQL query
        """
        pass

    def pool(self, pool_interval: int, pool_limit: int, **kwargs):
        """This method doesn't have be implemented by all sources.
        Implement this method if you want to poll something on a source like checking for new files in S3,
        or query to return a value
        """
        pass

    def connect(self, **kwargs):
        """This method doesn't have be implemented by all sources.
        Implement this method if you want to establish a connection to the source,
         and keep reusing the same connection across the job
        """
        pass

    def disconnect(self, **kwargs):
        """This method doesn't have be implemented by all sources.
        Implement this method if you want to close the connection to the source after the job is done
        """
        pass
