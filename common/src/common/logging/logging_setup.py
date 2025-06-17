import json
import logging
import logging.config
import pathlib


def setup_logging():
    """
    Setup logging
    """
    config_file = pathlib.Path(__file__).parent / "default_config.json"
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
