import os
import sys
import pandas as pd
import json
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from utils import logger
from utils import connections
from utils import context

directory = context.get_context(os.path.abspath(__file__))
config_file = f"{directory}/utils/configurations/config.json"
extraction_logger = logger \
  .setup_logger("extraction_logger", f"{directory}/logs/main.log")

def extract():
  try:
    with open(config_file, "r") as conf_file:
      config = json.load(conf_file)
  except FileNotFoundError as file_not_found_error:
    extraction_logger.error(f"Config file was not found: {file_not_found_error}")
    sys.exit(1)

  try:
    internal_engine = connections.engine_creation(
      server=config['Clarity - VH']['server'],
      db=config['Clarity - VH']['database'],
      driver=config['Clarity - VH']['driver'],
      internal_use=True
    )

    test_pats_sql = f"{directory}/sql/test_pats.sql"
    test_pats_csv = f"{directory}/data-raw/test_pats.csv"

    with internal_engine.connect() as clarity_connection:
      pats_not_seen_sql = connections.sql_to_df(file=test_pats_sql,
                                                connection=clarity_connection)

      with open(test_pats_csv, "wb") as staging_pats:
        pats_not_seen_sql.to_csv(staging_pats, index = False)
        extraction_logger.debug("Successfully staged test patients extract.")
  except ConnectionError as connection_error:
    extraction_logger.error(f"Unable to connect to db: {connection_error}")
    sys.exit(1)
  except KeyError as key_error:
    extraction_logger.error(f"Incorrect connection keys: {key_error}")
    sys.exit(1)

  extraction_logger.debug("Extraction complete.")
