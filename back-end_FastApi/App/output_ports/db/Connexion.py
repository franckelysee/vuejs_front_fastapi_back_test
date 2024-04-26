from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mariadb+mariadbconnector://elysee:elysee@localhost:3306/shoppy"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
      yield db
    except Exception as e:
      print(f'Something went wrong: {e}')
    finally:
      db.close()
   