from dotenv import load_dotenv
from pathlib import Path
import os
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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

    # Conexión al servidor de base de datos, no a una base de datos específica
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    engine = create_engine(connection_string)

    # Obtener una conexión directa al motor de base de datos
    conn = engine.raw_connection()
    try:
        # Necesario para poder ejecutar una sentencia de creación de base de datos
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Crear un cursor
        cur = conn.cursor()
        try:
            # Ejecutar la sentencia de creación de base de datos
            cur.execute(f"CREATE DATABASE {DB_NAME};")
        finally:
            # Cerrar siempre el cursor
            cur.close()
    finally:
        # Cerrar siempre la conexión
        conn.close()

    print(f"Database '{DB_NAME}' successfully created.")

except Exception as e:
    print(f"Error creating the database: {e}")