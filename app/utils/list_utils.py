from sqlmodel import Session, select
from app.models.secretsantalist import SecretSantaList
from app.db import engine

DEFAULT_LIST_NAME = "Default Secret Santa List"


def get_session():
    """
    This function provides a database session.
    """
    with Session(engine) as session:
        yield session


def get_default_list(session: Session) -> SecretSantaList:
    """
    This function retrieves or creates the default Secret Santa list if it doesn't exist.

    :param session: The database session to use for the query
    :return: The default Secret Santa list
    """
    # Try to find the default list
    default_list = session.exec(
        select(SecretSantaList).where(SecretSantaList.name == DEFAULT_LIST_NAME)
    ).first()

    # If not found, create the default list
    if not default_list:
        default_list = SecretSantaList(name=DEFAULT_LIST_NAME)
        session.add(default_list)
        session.commit()
        session.refresh(default_list)

    return default_list
