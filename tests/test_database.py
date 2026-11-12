from sqlalchemy import text
from sqlalchemy.orm import Session


def test_database_connection(db_session: Session):
    result = db_session.execute(
        text("SELECT current_database()")
    )

    database_name = result.scalar()

    assert database_name == "media_tracker_test"