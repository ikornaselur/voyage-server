import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
