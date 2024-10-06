from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = create_engine('sqlite+pysqlite:///s4e.db', echo=True)

Session = sessionmaker(_engine)

__all__ = ['Session']
