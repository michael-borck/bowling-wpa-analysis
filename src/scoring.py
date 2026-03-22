#!/usr/bin/env python3
"""
scoring.py

Scoring functions for traditional and World Bowling ten-pin bowling systems.

Ported from the skill-sequence-scoring project (Borck, 2026).
"""


def score_traditional(balls):
    """
    Score a complete game under traditional rules.
    balls: list of pin counts for each ball thrown in sequence.
    Returns integer score, or None if the sequence is invalid.
    """
    score = 0
    i = 0
    for frame in range(10):
        if i >= len(balls):
            return None
        if frame < 9:
            if balls[i] == 10:          # strike
                if i + 2 >= len(balls):
                    return None
                score += 10 + balls[i+1] + balls[i+2]
                i += 1
            else:
                if i + 1 >= len(balls):
                    return None
                if balls[i] + balls[i+1] > 10:
                    return None         # invalid
                score += balls[i] + balls[i+1]
                if balls[i] + balls[i+1] == 10:     # spare
                    if i + 2 >= len(balls):
                        return None
                    score += balls[i+2]
                i += 2
        else:   # frame 10
            if balls[i] == 10:          # strike
                if i + 2 >= len(balls):
                    return None
                b2 = balls[i+1]
                b3 = balls[i+2]
                if b2 == 10:
                    score += 10 + b2 + b3
                elif b2 + b3 > 10:
                    return None
                else:
                    score += 10 + b2 + b3
            else:
                if i + 1 >= len(balls):
                    return None
                if balls[i] + balls[i+1] > 10:
                    return None
                if balls[i] + balls[i+1] == 10:     # spare
                    if i + 2 >= len(balls):
                        return None
                    score += 10 + balls[i+2]
                else:
                    score += balls[i] + balls[i+1]
    return score


def score_world(balls):
    """
    Score a complete game under World Bowling (current-frame) rules.
    balls: list of pin counts for each ball thrown.
    Returns integer score, or None if invalid.
    """
    score = 0
    i = 0
    for frame in range(10):
        if i >= len(balls):
            return None
        if balls[i] == 10:              # strike
            score += 30
            i += 1
        else:
            if i + 1 >= len(balls):
                return None
            if balls[i] + balls[i+1] > 10:
                return None
            if balls[i] + balls[i+1] == 10:
                score += 10 + balls[i]  # spare
            else:
                score += balls[i] + balls[i+1]
            i += 2
    return score


def score_traditional_partial(balls):
    """
    Score a partial game under traditional rules.

    Returns a tuple (score, pending_bonuses) where:
      - score: the score so far (counting only fully resolved frames)
      - pending_bonuses: number of future balls still needed to resolve
        the current frame's bonus

    Useful for computing win probability at mid-game states.
    """
    score = 0
    i = 0
    frames_scored = 0

    for frame in range(10):
        if i >= len(balls):
            break
        if frame < 9:
            if balls[i] == 10:  # strike
                if i + 2 < len(balls):
                    score += 10 + balls[i+1] + balls[i+2]
                    frames_scored += 1
                else:
                    break  # can't fully score this frame yet
                i += 1
            else:
                if i + 1 >= len(balls):
                    break
                if balls[i] + balls[i+1] == 10:  # spare
                    if i + 2 < len(balls):
                        score += 10 + balls[i+2]
                        frames_scored += 1
                    else:
                        break
                else:
                    score += balls[i] + balls[i+1]
                    frames_scored += 1
                i += 2
        else:  # frame 10
            if balls[i] == 10:
                if i + 2 < len(balls):
                    score += 10 + balls[i+1] + balls[i+2]
                    frames_scored += 1
                else:
                    break
            else:
                if i + 1 >= len(balls):
                    break
                if balls[i] + balls[i+1] == 10:
                    if i + 2 < len(balls):
                        score += 10 + balls[i+2]
                        frames_scored += 1
                    else:
                        break
                else:
                    score += balls[i] + balls[i+1]
                    frames_scored += 1

    return score, frames_scored
