from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from modelledger.settings import get_settings


class Base(DeclarativeBase):
    pass


def make_engine(database_url: str | None = None):
    url = database_url or get_settings().database_url
    options = {"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {}
    if url == "sqlite:///:memory:":
        options["poolclass"] = StaticPool
    return create_engine(url, pool_pre_ping=True, future=True, **options)


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def create_schema() -> None:
    import modelledger.models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
