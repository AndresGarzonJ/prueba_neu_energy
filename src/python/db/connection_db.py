from dotenv import load_dotenv
from pathlib import Path
import sys
import os
from sqlalchemy import create_engine, Column, Integer, Float, ForeignKey, TIMESTAMP, ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
Session = None
session = None

def load_env_variables():
    current_dir = Path(__file__).parent
    env_path = current_dir / '..' / '..' / '..' / '.env'
    load_dotenv(dotenv_path=env_path)

    return {
        "db_user": os.getenv('DB_USER'),
        "db_password": os.getenv('DB_PASSWORD'),
        "db_host": os.getenv('DB_HOST'),
        "db_port": os.getenv('DB_PORT'),
        "db_name": os.getenv('DB_NAME')
    }

def create_db_engine(config):
    engine_url = f"postgresql://{config['db_user']}:{config['db_password']}@{config['db_host']}/{config['db_name']}"
    return create_engine(engine_url)

class Consumption(Base):
    __tablename__ = 'consumption'
    id_record = Column(Integer, ForeignKey('records.id_record'), primary_key=True)
    value = Column(Float)

class Injection(Base):
    __tablename__ = 'injection'
    id_record = Column(Integer, ForeignKey('records.id_record'), primary_key=True)
    value = Column(Float)

class XmDataHourlyPerAgent(Base):
    __tablename__ = 'xm_data_hourly_per_agent'
    record_timestamp = Column(TIMESTAMP, primary_key=True)
    value = Column(Float)

class Records(Base):
    __tablename__ = 'records'
    id_record = Column(Integer, primary_key=True)
    id_service = Column(Integer, ForeignKey('services.id_service'))
    record_timestamp = Column(TIMESTAMP, ForeignKey('xm_data_hourly_per_agent.record_timestamp'))

class Services(Base):
    __tablename__ = 'services'
    id_service = Column(Integer, primary_key=True)
    id_market = Column(Integer)
    cdi = Column(Integer)
    voltage_level = Column(Integer)
    __table_args__ = (
        ForeignKeyConstraint(['id_market', 'cdi', 'voltage_level'],
                            ['tariffs.id_market', 'tariffs.cdi', 'tariffs.voltage_level']),
    )

class Tariffs(Base):
    __tablename__ = 'tariffs'
    id_market = Column(Integer, primary_key=True)
    voltage_level = Column(Integer, primary_key=True)
    cdi = Column(Integer, primary_key=True)
    G = Column(Float)
    T = Column(Float)
    D = Column(Float)
    R = Column(Float)
    C = Column(Float)
    P = Column(Float)
    CU = Column(Float)


try:
    config = load_env_variables()
    engine = create_db_engine(config)

    try:
        if (sys.argv[1] == "create_tables"):
            Base.metadata.create_all(engine)
            print(f"Tables successfully created in the '{config['db_name']}' database.")
            engine.dispose()
            exit(1)
    except IndexError:
        print(f"Tables created previously in the '{config['db_name']}' database.")

    Session = sessionmaker(bind=engine)
    session = Session()
    # session.close()

except Exception as e:
    print(f"Error connecting to database: {e}")