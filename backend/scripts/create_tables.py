from app.database.session import engine, Base
from app import models

def create_all():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    print("Creating database tables...")
    create_all()
    print("Done")
