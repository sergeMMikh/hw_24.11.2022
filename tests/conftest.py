import pytest
import time

from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB
from models import Base, User
from auth import hash_password

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
Session = sessionmaker(bind=engine)


@pytest.fixture(scope='session', autouse=True)
def cleanup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield


@pytest.fixture(scope='session')
def root_user():
    with Session() as session:
        new_user = User(name='root',
                        password=hash_password('toor'),
                        email='toor@mmail.com')
        session.add(new_user)
        session.commit()
        return {
            'id': new_user.id,
            'name': new_user.name,
            'password': 'toor',
            'email': new_user.email
        }


@pytest.fixture()
def new_user():
    with Session() as session:
        time.sleep(0.001)
        new_user = User(name=f'new_user_{time.time()}',
                        password=hash_password('1234'),
                        email=f'{time.time()}@mmail.com')
        try:
            session.add(new_user)
        except:
            session.rollback()
        session.commit()
        return {
            'id': new_user.id,
            'name': new_user.name,
            'password': '1234',
            'email': new_user.email
        }
