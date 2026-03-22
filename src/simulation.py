#!/usr/bin/env python3
"""
simulation.py

Monte Carlo simulation of bowling games at different skill levels.

Ported from the skill-sequence-scoring project (Borck, 2026).
Uses a first-order Markov chain for strike probability transitions
and leave-dependent spare difficulty classes.

Model:
  Each ball is modelled with skill-dependent probabilities:
    - Strike probability (p_strike): probability of knocking all 10 pins
    - Spare probability (p_spare): probability of converting remaining pins
    - Pin distribution: when not striking, first ball pins follow a
      truncated distribution shaped by skill level

  Skill tiers (calibrated from USBC/PBA statistics):
    - Recreational:  p_strike ~ 0.04, p_spare ~ 0.27
    - Club:          p_strike ~ 0.20, p_spare ~ 0.47
    - Competitive:   p_strike ~ 0.40, p_spare ~ 0.64
    - Elite:         p_strike ~ 0.55, p_spare ~ 0.77
    - Professional:  p_strike ~ 0.66, p_spare ~ 0.86
    - Top 10:        p_strike ~ 0.73, p_spare ~ 0.92
"""

import numpy as np

from .scoring import score_traditional, score_world


# ── Player Model ─────────────────────────────────────────────────────────────

SKILL_TIERS = {
    'Recreational': {'p_strike': 0.04, 'p_spare': 0.27, 'pin_mean': 4.2},
    'Club':         {'p_strike': 0.20, 'p_spare': 0.47, 'pin_mean': 5.5},
    'Competitive':  {'p_strike': 0.40, 'p_spare': 0.64, 'pin_mean': 6.5},
    'Elite':        {'p_strike': 0.55, 'p_spare': 0.77, 'pin_mean': 7.2},
    'Professional': {'p_strike': 0.66, 'p_spare': 0.86, 'pin_mean': 7.8},
    'Top 10':       {'p_strike': 0.73, 'p_spare': 0.92, 'pin_mean': 8.2},
}


# ── Spare Difficulty Classes ─────────────────────────────────────────────────

# Spare difficulty classes: proportion of non-strike leaves that fall into each
# category, and the conversion rate for each. Based on PBA spare conversion
# data reported in Keogh & O'Neill (2011) and general bowling analytics.
SPARE_CLASSES = {
    # (proportion_of_leaves, conversion_rate_multiplier)
    # Multiplier is applied to base p_spare
    'easy':     (0.55, 1.10),   # single-pin leaves (e.g., 7, 10, 5)
    'moderate': (0.35, 0.90),   # multi-pin clusters (e.g., 3-6, 2-4-5)
    'split':    (0.10, 0.30),   # splits (e.g., 7-10, 4-6-7-10)
}


# ── Ball Simulation ──────────────────────────────────────────────────────────

def simulate_first_ball(rng, p_strike, pin_mean):
    """
    Simulate first ball of a frame.
    Returns number of pins knocked down (0-10).
    """
    if rng.random() < p_strike:
        return 10

    # Non-strike: draw from a beta-binomial-like distribution
    # Use a simple approach: sample from binomial(10, pin_mean/10)
    # but exclude 10 (already handled as strike)
    p_pin = min(pin_mean / 10.0, 0.95)
    pins = rng.binomial(10, p_pin)
    while pins == 10:
        pins = rng.binomial(10, p_pin)
    return int(pins)


def simulate_second_ball(rng, first_ball, p_spare):
    """
    Simulate second ball given first ball result.
    Returns number of additional pins knocked down.
    """
    remaining = 10 - first_ball
    if remaining == 0:
        return 0

    if rng.random() < p_spare:
        return remaining  # spare

    # Not a spare: knock down some of the remaining pins
    # Use uniform-ish distribution over 0..remaining-1
    pins = rng.integers(0, remaining)  # excludes remaining (not a spare)
    return int(pins)


def simulate_second_ball_difficulty(rng, first_ball, p_spare):
    """
    Simulate second ball with leave-dependent spare conversion.
    Harder leaves (splits) are much less likely to be converted.
    """
    remaining = 10 - first_ball
    if remaining == 0:
        return 0

    # Classify the leave
    r = rng.random()
    if r < SPARE_CLASSES['easy'][0]:
        p_eff = min(p_spare * SPARE_CLASSES['easy'][1], 0.99)
    elif r < SPARE_CLASSES['easy'][0] + SPARE_CLASSES['moderate'][0]:
        p_eff = p_spare * SPARE_CLASSES['moderate'][1]
    else:
        p_eff = p_spare * SPARE_CLASSES['split'][1]

    if rng.random() < p_eff:
        return remaining  # spare

    # Not a spare — knock down some remaining pins
    pins = rng.integers(0, remaining)
    return int(pins)


# ── Game Simulation (Markov Chain Model) ─────────────────────────────────────

def simulate_game_markov(rng, p_strike, p_spare, pin_mean,
                         p_strike_after_strike=None,
                         p_strike_after_spare=None,
                         p_strike_after_open=None):
    """
    Simulate one game using a first-order Markov chain for strike probability.

    Transition probabilities:
      P(strike | previous frame was strike) = p_strike_after_strike
      P(strike | previous frame was spare)  = p_strike_after_spare
      P(strike | previous frame was open)   = p_strike_after_open

    If not provided, defaults are derived from the base strike rate using
    empirical ratios from Yaari & Eisenmann (2012):
      - After strike: base * 1.15 (positive autocorrelation)
      - After spare:  base * 0.95 (slight reset)
      - After open:   base * 0.85 (negative momentum)

    Spare conversion uses leave-dependent difficulty classes.
    """
    # Set transition probabilities
    if p_strike_after_strike is None:
        p_strike_after_strike = min(p_strike * 1.15, 0.95)
    if p_strike_after_spare is None:
        p_strike_after_spare = p_strike * 0.95
    if p_strike_after_open is None:
        p_strike_after_open = p_strike * 0.85

    balls = []
    prev_result = 'open'  # start with no momentum

    # Frames 1-9
    for _ in range(9):
        # Select strike probability based on previous frame outcome
        if prev_result == 'strike':
            ps = p_strike_after_strike
        elif prev_result == 'spare':
            ps = p_strike_after_spare
        else:
            ps = p_strike_after_open

        b1 = simulate_first_ball(rng, ps, pin_mean)
        balls.append(b1)

        if b1 == 10:
            prev_result = 'strike'
        else:
            b2 = simulate_second_ball_difficulty(rng, b1, p_spare)
            balls.append(b2)
            prev_result = 'spare' if b1 + b2 == 10 else 'open'

    # Frame 10
    if prev_result == 'strike':
        ps = p_strike_after_strike
    elif prev_result == 'spare':
        ps = p_strike_after_spare
    else:
        ps = p_strike_after_open

    b1 = simulate_first_ball(rng, ps, pin_mean)
    balls.append(b1)

    if b1 == 10:
        ps10 = p_strike_after_strike
        b2 = simulate_first_ball(rng, ps10, pin_mean)
        balls.append(b2)
        if b2 == 10:
            b3 = simulate_first_ball(rng, ps10, pin_mean)
            balls.append(b3)
        else:
            b3 = simulate_second_ball_difficulty(rng, b2, p_spare)
            balls.append(b3)
    else:
        b2 = simulate_second_ball_difficulty(rng, b1, p_spare)
        balls.append(b2)
        if b1 + b2 == 10:
            b3 = simulate_first_ball(rng, p_strike_after_spare, pin_mean)
            balls.append(b3)

    return balls


def simulate_games_markov(n_games, p_strike, p_spare, pin_mean, seed=42):
    """Simulate n_games with Markov chain model and spare difficulty."""
    rng = np.random.default_rng(seed)
    trad_scores = []
    world_scores = []

    for _ in range(n_games):
        balls = simulate_game_markov(rng, p_strike, p_spare, pin_mean)
        t = score_traditional(balls)
        w = score_world(balls)
        if t is not None and w is not None:
            trad_scores.append(t)
            world_scores.append(w)

    return np.array(trad_scores), np.array(world_scores)
