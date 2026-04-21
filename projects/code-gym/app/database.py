"""
code-gym database setup
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import os, sys
# Resolve models.Base — app/ is a package, models is inside it
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)
from models import Base

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "codegym.db")
DATA_DIR = os.path.dirname(DATABASE_PATH)

def get_engine():
    os.makedirs(DATA_DIR, exist_ok=True)
    return create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)

def get_session():
    engine = get_engine()
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))
    return Session

def init_db():
    """Create all tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)
