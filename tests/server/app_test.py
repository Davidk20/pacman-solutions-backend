"""Tests for the Flask application."""


def test_app(client):
    """Basic test to check functionality of root page."""
    response = client.get("/")
    print(response)
    assert response.status_code == 303


def test_get_invalid_board(client):
    """Test that a 400 status code is given when level_num is invalid."""
    response = client.get("/get-game?level_num=123456")
    assert response.status == "400 BAD REQUEST"


def test_get_overview(client):
    """Test that the levels overview is correctly returned."""
    response = client.get("/get-levels")
    assert b'["Level 1"]\n' in response.data
