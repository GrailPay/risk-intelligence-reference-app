from typing import Generator

import pytest

from app import create_app


@pytest.fixture
def test_app() -> Generator:
    app = create_app()

    with app.app_context():
        yield app
