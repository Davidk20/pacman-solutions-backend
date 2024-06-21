"""Tests for the pickups in the game."""

from src.models.pickups import (
    Apple,
    Bell,
    Cherry,
    Galaxian,
    Key,
    Melon,
    Orange,
    PacDot,
    PowerPellet,
    Strawberry,
)


def test_get_score():
    """Tests that the items all have the correct score"""
    assert PacDot().score == 10
    assert PowerPellet().score == 50
    assert Cherry().score == 100
    assert Strawberry().score == 300
    assert Orange().score == 500
    assert Apple().score == 700
    assert Melon().score == 1000
    assert Galaxian().score == 2000
    assert Bell().score == 3000
    assert Key().score == 5000
