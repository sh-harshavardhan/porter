"""local"""

from src.sources.base import Source


class FileSource(Source):
    """LocalFile source"""

    def is_source(self):
        """Is source"""
        return True

    def is_target(self):
        """Is source"""
        return True
