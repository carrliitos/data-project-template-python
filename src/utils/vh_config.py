import os
import os.path
import json

from utils import context

directory = context.get_context(os.path.abspath(__file__))
config_file = f"{directory}/utils/config/config.json"
tableau_config_file = f"{directory}/utils/config/tableau_project_ids.json"

def grab(logger):
    """
    A helper function to grab that configuration file.
    """

    try:
        with open(config_file, "r") as conf_file:
            conf = json.load(conf_file)
    except FileNotFoundError as file_not_found_error:
        logger.error(f"Config file was not found: {file_not_found_error}")

    return conf


def grab_tableau_id(project_name, logger):
    """
    A helper function to grab those Tableau Project IDs.
    """

    try:
        with open(tableau_config_file, "r") as project_ids:
            proj_id = json.load(project_ids)
    except FileNotFoundError as file_not_found_error:
        logger.error(f"Tableau Project IDs JSON file not found: {file_not_found_error}")

    return proj_id[project_name]["project_id"]
