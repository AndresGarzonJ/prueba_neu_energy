from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine

try:
    # Get the path to the current directory where the script is located
    current_dir = Path(__file__).parent
    env_path = current_dir / '..' / '..' / '..' / '.env'

    # Load environment variables from the .env file
    load_dotenv(dotenv_path=env_path)
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    engine = create_engine('postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))

    df_tariffs = pd.read_csv('../../../data/tariffs.csv')
    # Replace NaN values (including those represented by ,, in the CSV) in the entire DataFrame with 101
    df_tariffs.fillna(101, inplace=True) 
    df_tariffs.columns = ['id_market', 'voltage_level', 'cdi', 'G', 'T', 'D', 'R', 'C', 'P', 'CU']

    df_services = pd.read_csv('../../../data/services.csv')
    df_services.columns = ['id_service', 'id_market', 'cdi', 'voltage_level']

    df_xm_data_hourly_per_agent = pd.read_csv('../../../data/xm_data_hourly_per_agent.csv')
    df_xm_data_hourly_per_agent.columns = ['record_timestamp', 'value']

    df_records = pd.read_csv('../../../data/records.csv')
    df_records.columns = ['id_record', 'id_service', 'record_timestamp']

    df_consumption = pd.read_csv('../../../data/consumption.csv')
    df_consumption.columns = ['id_record', 'value']

    df_injection = pd.read_csv('../../../data/injection.csv')
    df_injection.columns = ['id_record', 'value']

    # Upload data into the database
    df_tariffs.to_sql('tariffs', con=engine, if_exists='append', index=False)
    df_services.to_sql('services', con=engine, if_exists='append', index=False)
    df_xm_data_hourly_per_agent.to_sql('xm_data_hourly_per_agent', con=engine, if_exists='append', index=False)
    df_records.to_sql('records', con=engine, if_exists='append', index=False)
    df_consumption.to_sql('consumption', con=engine, if_exists='append', index=False)
    df_injection.to_sql('injection', con=engine, if_exists='append', index=False)

    print(f"Data successfully uploaded to the '{DB_NAME}' database.")

except Exception as e:
    print(f"Error uploading data to the database: {e}")
finally:
    engine.dispose()
