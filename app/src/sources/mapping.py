"""This is a mapping file which maps the source_type to the Source implementation"""

from src.sources.file.local.local_source import FileSource

sources_mapping = {
    "file": FileSource,
}
