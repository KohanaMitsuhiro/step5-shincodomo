from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()

# 環境変数から接続情報を取得
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()