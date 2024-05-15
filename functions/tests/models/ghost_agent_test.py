"""Tests for the Ghost Agent."""
import pytest
from tests.mocks.mock_agent_test import mock_ghost


@pytest.fixture(autouse=True)
def ghost():
    """Generate an agent of a Ghost which can be used for testing."""
    yield mock_ghost()
