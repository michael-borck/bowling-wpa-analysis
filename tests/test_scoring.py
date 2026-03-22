"""Basic tests for scoring functions."""

from src.scoring import score_traditional, score_world


def test_perfect_game_traditional():
    assert score_traditional([10] * 12) == 300


def test_perfect_game_world():
    assert score_world([10] * 10) == 300


def test_all_spares_traditional():
    balls = [5, 5] * 10 + [5]
    assert score_traditional(balls) == 150


def test_all_spares_world():
    balls = [5, 5] * 10
    assert score_world(balls) == 150


def test_all_open_traditional():
    balls = [4, 3] * 10
    assert score_traditional(balls) == 70


def test_all_open_world():
    balls = [4, 3] * 10
    assert score_world(balls) == 70
