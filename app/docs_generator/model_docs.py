"""Generates markdown documentation for dataset models using Jinja2 templates."""

import yaml
from jinja2 import Environment, BaseLoader
from pathlib import Path

from src.common.base_logger import log
from src.models.dataset.table import TableDataset
from src.models.dataset.api import ApiDataset
from src.models.dataset.file import FileDataset


# print(json.loads(schema_json_of(TableDataset)))
# print(TableDataset.model_json_schema())
# print(TableDataset.model_json_schema().keys())
# for field_name, field_values in TableDataset.model_json_schema().get('properties').items():
#     print(field_name, field_values)


def to_yaml(data):
    """Converts a Python dictionary or list to a YAML string."""
    return (
        yaml.dump(data, sort_keys=False).replace("\n", "<br>").replace("\t", "&emsp;")
    )


def main():
    """Generates markdown documentation for dataset models."""
    environment = Environment(loader=BaseLoader())
    environment.filters["to_yaml"] = to_yaml  # Register the filter

    with open("template.md") as r_fp:
        template_content = r_fp.read()
        template = environment.from_string(template_content)

    current_path = Path(__file__).resolve()
    docs_path = Path(current_path.parent.parent.parent, "docs", "models", "dataset")
    Path(docs_path).mkdir(parents=True, exist_ok=True)

    for dataset_class in [TableDataset, ApiDataset, FileDataset]:
        rendered_output = template.render(
            spec=dataset_class.model_json_schema(),
        )
        file_name = Path(docs_path, f"{dataset_class.__name__}.md")
        log.info(f"Writing documentation for {dataset_class.__name__} to {file_name}")
        with open(file_name, "w") as w_fp:
            w_fp.write(rendered_output)


if __name__ == "__main__":
    main()
