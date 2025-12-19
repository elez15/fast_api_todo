# Things what we do in database table
# those things will be done through class file
# this is called ORM model

from sqlalchemy import Column, Integer, String, Boolean
from database import custom_base


class TodoModel(custom_base):
    __tablename__ = "Todos"  # This attribute tells SQLAlchemy the name of the specific table in our database that this Python class to map.
    # primary key, type of value, database indexing required or not
    id = Column(Integer, primary_key=True, index=True)  # table setup
    # title cannot be nalluable
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
