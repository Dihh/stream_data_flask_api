import pytest
from app import create_app
from db import db


@pytest.fixture()
def clean_data():
    with create_app().app_context():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
    yield
