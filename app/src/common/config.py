"""Config related functions"""

import yaml
import json
from pathlib import Path
from typing import Any
from src.common.base_logger import log


def read_config_file(
    file_path: str,
    model: Any,
) -> Any:
    """Parse the YAML/JSON and validate against the Pydantic Base model that is passed and return the parsed obj"""
    with open(file_path) as r_fp:
        try:
            if Path(file_path).suffix == ".yaml":
                yaml_config = yaml.safe_load(r_fp.read())
                config = model.parse_obj(yaml_config)
            elif Path(file_path).suffix == ".json":
                json_config = json.load(r_fp)
                config = model.parse_obj(json_config)
            else:
                raise Exception(f"File type: {Path(file_path).suffix} is not supported")
        except yaml.YAMLError as ye:
            log.error(ye)
            raise RuntimeError(
                f"Could not parse the YAML file: {file_path} into {model.__class__.__name__}"
            )
        except json.JSONDecodeError as je:
            log.error(je)
            raise RuntimeError(
                f"Could not parse the JSON file: {file_path} into {model.__class__.__name__}"
            )
        except Exception as e:
            log.error(
                f"UNKNOWN Exception while parsing the file: {file_path} into {model.__class__.__name__} "
            )
            raise e

    return config
