import os
import os.path
import json

import tableauserverclient as TSC
from tableauhyperapi import (
    HyperProcess,
    Connection,
    Telemetry,
    Inserter,
    CreateMode,
    escape_string_literal
)

from utils import vh_config

def push_to_tableau(df, hyper_file, table_definition, logger, project_id):
    """
    Converts a Pandas dataframe to a Tableau Hyper file.
    Once conversion is finished, it pushes the newly created (or overwritten) 
    Tableau Hyper file to Tableau Server.

    :param df: Pandas dataframe
    :param hyper_file: Path to Tableau Hyper File
    :param table_definition: SQL table definition
    :param logger: Workflow logger
    :param project_id: Tableau Project ID
    """
    logger.info(f"Creating Hyper file: {hyper_file}")

    with HyperProcess(telemetry = Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU,
                      parameters = {"log_config": ""}) as hyper_process:
        with Connection(endpoint = hyper_process.endpoint,
                        create_mode = CreateMode.CREATE_AND_REPLACE,
                        database = hyper_file) as connection:
            connection.catalog.create_schema("Extract")
            connection.catalog.create_table(table_definition)

            with Inserter(connection, table_definition) as inserter:
                for index, row in df.iterrows():
                    inserter.add_row(row)
                inserter.execute()

    logger.info("Connection to Hyper file is closed.")

    logger.info(f"Publishing Hyper filer ('{hyper_file}') to Tableau.")
    publish_data_source(project_id, logger, hyper_file)


def publish_data_source(project_id, logger, hyper_file):
    """
    Publishes the newly created Hyper file to the Tableau Server.

    :param project_id: Tableau Project ID
    :param logger: Workflow logger
    :param hyper_file: Path to Tableau Hyper File
    """
    config = vh_config.grab(logger)

    server = config["TableauCloud"]["server"]
    token_name = config["TableauCloud"]["token_name"]
    token_value = config["TableauCloud"]["token_value"]
    site_url_name = config["TableauCloud"]["siteid"]

    tableau_auth = TSC.PersonalAccessTokenAuth(token_name,
                                               token_value,
                                               site_id=site_url_name)
    tableau_server = TSC.Server(server, use_server_version = True)

    with tableau_server.auth.sign_in(tableau_auth):
        datasource = TSC.DatasourceItem(project_id = project_id)
        publish_mode = TSC.Server.PublishMode.Overwrite

        new_datasource = tableau_server.datasources.publish(
            datasource, hyper_file, publish_mode
        )

        ds_id = new_datasource.id
        logger.info(f"Datasource published. Datasource ID: {ds_id}")
