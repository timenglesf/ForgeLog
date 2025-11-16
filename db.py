from sqlalchemy import create_engine, Engine

from config import sqlite_engine_uri


# Create Connection to sqlite
_engine = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(sqlite_engine_uri, echo=False, future=True)
    return _engine
