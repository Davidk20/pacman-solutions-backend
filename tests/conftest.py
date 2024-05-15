"""
Configuration file allowing a test instance of the Flask server to be created.
"""

import pytest
from src.server import server


@pytest.fixture()
def app():
    """Create fixture of flask application so that it can be tested."""
    app = server.app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    """
    Return a test instance of the app so that it can be
    directly used by the tests.
    """
    return app.test_client()
