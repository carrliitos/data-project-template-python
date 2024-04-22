from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd

def engine_creation(uid=None, 
                    pwd=None, 
                    server=None, 
                    db=None, 
                    driver="ODBC Driver 17 for SQL Server",
                    internal_use=False):
    """
    Creates SQLAlchemy engine to be used for database connections

    :param uid: Username ID
    :param pwd: Password
    :param server: Server name
    :param db: Database name
    :param driver: Driver name. Defaults to ODBC Driver 17 for SQL Server.
    :param internal_use: Determines if the internal Clarity server is being 
    accessed.
    """
    if internal_use:
        return create_engine(f"mssql+pyodbc://{server}/{db}?trusted_connection=yes&driver={driver}")
    else:
        connection_url = URL.create(
            "mssql+pyodbc",
            username=uid,
            password=pwd,
            host=server,
            database=db
        )
        return create_engine(f"{connection_url}?driver={driver}")


def sql_to_df(file, connection):
    """
    Reads in SQL files and convert them to Pandas dataframe
    
    :param file: SQL file to access.
    :param connection: Database connection
    """
    with open(file, 'r') as sql_file:
        df = pd.read_sql_query(sql_file.read(), connection)

    return df