#!/usr/bin/env python3
"""
wpa_engine.py

Win Probability Added (WPA) and Leverage Index engine for ten-pin bowling.

Computes win probability for any game state under both traditional and
World Bowling scoring systems, enabling analysis of competitive dynamics
and high-leverage moments in head-to-head matches.

Key concepts:
  - Game state: (frame, ball, score_A, score_B, pending_bonuses_A,
    pending_bonuses_B) — everything needed to compute P(A wins)
  - Win Probability (WP): P(player A wins) at a given game state
  - Win Probability Added (WPA): change in WP caused by a single ball
  - Leverage Index (LI): expected absolute WPA of the next ball —
    how much the next ball is expected to shift the outcome

References:
  - Borck (2026), "Skill, Sequence, and Scoring" — scoring functions
    and Markov simulation model
  - VanDerwerken & Kenter (2018), JQAS — Markov bowling model
  - Tango, Lichtman, & Dolphin (2007) — Leverage Index concept
  - FanGraphs WPA methodology (adapted from baseball to bowling)
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np


# ── Game State Representation ────────────────────────────────────────────────

@dataclass
class GameState:
    """
    Complete state of a head-to-head bowling match at a point in time.

    Attributes:
        frame: Current frame number (1-10).
        ball: Ball within the current frame (1 or 2; up to 3 in frame 10).
        score_a: Player A's current confirmed score.
        score_b: Player B's current confirmed score.
        balls_a: Player A's ball sequence so far.
        balls_b: Player B's ball sequence so far.
        frames_completed_a: Number of fully scored frames for player A.
        frames_completed_b: Number of fully scored frames for player B.
        scoring_system: 'traditional' or 'world'.
    """
    frame: int
    ball: int
    score_a: int
    score_b: int
    balls_a: list
    balls_b: list
    frames_completed_a: int
    frames_completed_b: int
    scoring_system: str = 'traditional'


# ── Win Probability Computation ──────────────────────────────────────────────

def compute_win_probability(state, p_strike, p_spare, pin_mean,
                            n_simulations=10_000, seed=None):
    """
    Estimate P(player A wins) from a given game state using Monte Carlo
    simulation.

    Simulates the remainder of the game `n_simulations` times from the
    current state, using the Markov chain model, and returns the fraction
    of simulations where player A's final score exceeds player B's.

    Parameters:
        state: GameState — current match state.
        p_strike: Base strike probability for remaining simulation.
        p_spare: Base spare probability for remaining simulation.
        pin_mean: Mean first-ball pin count for remaining simulation.
        n_simulations: Number of Monte Carlo completions.
        seed: Random seed for reproducibility.

    Returns:
        float: Estimated P(A wins), in [0, 1].

    TODO: Implement full game-completion logic from partial state.
    """
    raise NotImplementedError


def compute_win_probability_exact(state, p_strike, p_spare, pin_mean):
    """
    Compute P(player A wins) exactly using dynamic programming over
    the state space.

    Only feasible for World Bowling scoring (smaller state space due to
    no cross-frame bonuses). For traditional scoring, falls back to
    Monte Carlo.

    Parameters:
        state: GameState — current match state.
        p_strike: Base strike probability.
        p_spare: Base spare probability.
        pin_mean: Mean first-ball pin count.

    Returns:
        float: Exact P(A wins), in [0, 1].

    TODO: Implement DP over World Bowling state space.
    """
    raise NotImplementedError


# ── Win Probability Added ────────────────────────────────────────────────────

def compute_wpa(state_before, state_after, p_strike, p_spare, pin_mean,
                n_simulations=10_000, seed=None):
    """
    Compute Win Probability Added for a single ball.

    WPA = WP(after) - WP(before)

    A positive WPA means the ball helped player A; negative means it
    helped player B (or hurt A).

    Parameters:
        state_before: GameState before the ball was thrown.
        state_after: GameState after the ball was thrown.
        p_strike: Base strike probability for simulation.
        p_spare: Base spare probability for simulation.
        pin_mean: Mean first-ball pin count.
        n_simulations: Number of Monte Carlo completions per state.
        seed: Random seed.

    Returns:
        float: WPA value, in [-1, 1].

    TODO: Implement using compute_win_probability.
    """
    raise NotImplementedError


# ── Leverage Index ───────────────────────────────────────────────────────────

def compute_leverage_index(state, p_strike, p_spare, pin_mean,
                           n_simulations=10_000, seed=None):
    """
    Compute the Leverage Index for the next ball at a given game state.

    LI = E[|WPA|] for the next ball, normalised so that the average LI
    across all balls in a game equals 1.0.

    High LI means the next ball will have a large expected impact on
    the match outcome. Low LI means the match is already effectively
    decided.

    Parameters:
        state: GameState — current match state.
        p_strike: Base strike probability.
        p_spare: Base spare probability.
        pin_mean: Mean first-ball pin count.
        n_simulations: Number of Monte Carlo completions.
        seed: Random seed.

    Returns:
        float: Leverage Index (unnormalised). Normalisation constant
        should be computed from a full-game average.

    TODO: Implement by simulating possible next-ball outcomes and
    computing E[|WPA|].
    """
    raise NotImplementedError


# ── Full-Game WPA Trace ──────────────────────────────────────────────────────

def simulate_match_with_wpa(p_strike_a, p_spare_a, pin_mean_a,
                            p_strike_b, p_spare_b, pin_mean_b,
                            scoring_system='traditional',
                            n_wpa_sims=10_000, seed=None):
    """
    Simulate a full head-to-head match and compute WPA + LI for every ball.

    Both players bowl a complete game. After each ball, we compute the
    win probability and leverage index, producing a complete WPA trace
    suitable for plotting.

    Parameters:
        p_strike_a, p_spare_a, pin_mean_a: Player A skill parameters.
        p_strike_b, p_spare_b, pin_mean_b: Player B skill parameters.
        scoring_system: 'traditional' or 'world'.
        n_wpa_sims: Simulations per WP estimate.
        seed: Random seed.

    Returns:
        dict with keys:
            'balls_a': list of Player A's balls
            'balls_b': list of Player B's balls
            'wp_trace': list of P(A wins) after each ball (both players)
            'wpa_trace': list of WPA values for each ball
            'li_trace': list of Leverage Index values for each ball
            'final_score_a': int
            'final_score_b': int
            'winner': 'A', 'B', or 'tie'

    TODO: Implement full match simulation with WPA tracking.
    """
    raise NotImplementedError


# ── Leverage Profile Analysis ────────────────────────────────────────────────

def compute_leverage_profile(n_matches, p_strike, p_spare, pin_mean,
                             scoring_system='traditional',
                             n_wpa_sims=5_000, seed=None):
    """
    Compute the average leverage index at each frame position across
    many simulated matches between equal-skill opponents.

    This produces the "leverage profile" — showing which frames tend to
    be the most consequential under each scoring system.

    Parameters:
        n_matches: Number of matches to simulate.
        p_strike: Strike probability (same for both players).
        p_spare: Spare probability (same for both players).
        pin_mean: Mean first-ball pins (same for both players).
        scoring_system: 'traditional' or 'world'.
        n_wpa_sims: Simulations per WP estimate.
        seed: Random seed.

    Returns:
        dict with keys:
            'frame_numbers': array of frame positions (1-10)
            'mean_leverage': mean LI at each frame
            'std_leverage': std dev of LI at each frame
            'max_leverage': max observed LI at each frame

    TODO: Implement by running many matches and aggregating LI by frame.
    """
    raise NotImplementedError


def compare_leverage_profiles(n_matches, p_strike, p_spare, pin_mean,
                              n_wpa_sims=5_000, seed=None):
    """
    Compare leverage profiles between traditional and World Bowling
    scoring for equal-skill opponents.

    This is the core comparison for the paper: does traditional scoring
    create more high-leverage moments?

    Parameters:
        n_matches: Number of matches per scoring system.
        p_strike: Strike probability.
        p_spare: Spare probability.
        pin_mean: Mean first-ball pins.
        n_wpa_sims: Simulations per WP estimate.
        seed: Random seed.

    Returns:
        dict with keys:
            'traditional': leverage profile dict
            'world': leverage profile dict
            'leverage_ratio': traditional mean LI / world mean LI per frame

    TODO: Implement using compute_leverage_profile for both systems.
    """
    raise NotImplementedError


# ── Clutch Moment Analysis ───────────────────────────────────────────────────

def identify_clutch_moments(wpa_trace, li_trace, threshold_percentile=90):
    """
    Identify "clutch moments" — balls where the leverage index exceeds
    a given percentile threshold.

    Parameters:
        wpa_trace: list of WPA values from a match.
        li_trace: list of LI values from a match.
        threshold_percentile: percentile above which a moment is "clutch".

    Returns:
        list of dicts, each with:
            'ball_index': position in the match
            'leverage': LI value
            'wpa': WPA value
            'delivered': bool — did the player deliver under pressure?
              (True if WPA > 0, meaning the ball helped the active player)

    TODO: Implement clutch moment identification and classification.
    """
    raise NotImplementedError


def clutch_frequency_comparison(n_matches, p_strike, p_spare, pin_mean,
                                threshold_percentile=90,
                                n_wpa_sims=5_000, seed=None):
    """
    Compare the frequency and magnitude of clutch moments between
    scoring systems.

    Key question: does traditional scoring produce more situations where
    a single ball can dramatically change the match outcome?

    Parameters:
        n_matches: Number of matches per system.
        p_strike, p_spare, pin_mean: Skill parameters.
        threshold_percentile: Clutch threshold.
        n_wpa_sims: Simulations per WP estimate.
        seed: Random seed.

    Returns:
        dict with keys:
            'traditional_clutch_freq': avg clutch moments per match
            'world_clutch_freq': avg clutch moments per match
            'traditional_mean_li': mean LI of clutch moments
            'world_mean_li': mean LI of clutch moments
            'traditional_max_wpa': largest single-ball WPA observed
            'world_max_wpa': largest single-ball WPA observed

    TODO: Implement using simulate_match_with_wpa and
    identify_clutch_moments.
    """
    raise NotImplementedError
