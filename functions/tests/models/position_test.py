"""Tests for the Position class."""

from src.models.position import Position


def test_add():
    """Test the ability to add to a position."""
    p1 = Position(1, 1)
    p2 = Position(4, 7)
    assert p1.add(p2) == Position(5, 8)


def test_sub():
    """Test the ability to subtract from a position."""
    p1 = Position(4, 7)
    p2 = Position(1, 1)
    assert p1.subtract(p2) == Position(3, 6)


def test_multiply():
    """Test the ability to multiply a position"""
    pos = Position(1, 1)
    assert pos.multiply(4) == Position(4, 4)


def test_direct_distance():
    """
    Test that the direct distance is correctly calculated.
    """
    p1 = Position(1, 2)
    p2 = Position(1, 1)
    assert p1.direct_distance(p2) == Position(0, 1)
    p1 = Position(1, 2)
    assert p2.direct_distance(p1) == Position(0, -1)


def test_euclidean_distance():
    """
    Test that distance is correctly calculated.

    As floats should not be compared directly, comparison is made
    by checking the difference is within a tolerable range.
    """
    p1 = Position(1, 1)
    p2 = Position(4, 7)
    assert p1.euclidean_distance(p2) - 6.7082 <= 0.0001
