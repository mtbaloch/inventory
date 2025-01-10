from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from app.models.users import User
from app.models.products import Product
from app.core.config import settings


class DATABASE:
    # create constructor function
    # when class is used, below dunder function will run automatically
    def __init__(self, db_url: str):
        self.db_url = db_url.replace('postgresql', 'postgresql+psycopg2')
        self.engine = create_engine(db_url)
        
    def init_db(self) -> None:
        try:
            print("Start creating database tables")
            SQLModel.metadata.create_all(self.engine)
            print("Database tables created successfully")
        except Exception as e:
            print(f"Failed to create database tables: {e}")
            raise
    
    def db_session(self) -> Generator[Session, None, None]:
            with Session(self.engine) as session:
                try:
                  yield session
                except Exception as e:
                    print(f"failed to create database session: {e}")
                    raise
                finally:
                    session.close()

db = DATABASE(settings.DATABASE_URL)

def init_db()->None:
    db.init_db()

def db_session()-> Generator[Session, None, None]:
    yield from db.db_session()