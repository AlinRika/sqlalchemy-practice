from contextlib import contextmanager

from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

SQL_DATABASE_URL = 'sqlite://'
engine = create_engine(SQL_DATABASE_URL, echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'starwars'

    id: Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(200), unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def add_user(name):
    with get_session() as session:
        new_user = User(name=name)
        session.add(new_user)


def test_add_user():
    test_name = "Luke Skywalker"
    add_user(test_name)

    with get_session() as session:
        result = session.query(User).first()
        session.delete(result)
    assert result.name == test_name



