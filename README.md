# Win Probability and Leverage in Ten-Pin Bowling Scoring Systems

Research project analysing how scoring system design (traditional vs. World Bowling)
affects win probability dynamics and competitive leverage in head-to-head ten-pin bowling.

**Paper title:** "Win Probability and Leverage: How Scoring System Design Shapes
Competitive Dynamics in Ten-Pin Bowling"

**Target journal:** Journal of Quantitative Analysis in Sports

## Background

This is a follow-up to [Borck (2026)](https://github.com/michael-borck/skill-sequence-scoring),
which established that traditional scoring encodes more information about sustained
skill performance than World Bowling scoring. This project extends that analysis to
head-to-head competition, asking: how does each scoring system affect win probability
at each game state, and does traditional scoring create more high-leverage moments?

## Project Structure

```
bowling-wpa-analysis/
  data/          Simulation outputs and processed datasets
  src/           Source code
    scoring.py       Scoring functions (traditional + World Bowling)
    simulation.py    Game simulation engine (Markov chain model)
    wpa_engine.py    Win probability and leverage computation
  notebooks/     Exploratory analysis notebooks
  figures/       Generated figures for the paper
  paper/         Manuscript and research plan
  references/    Key reference papers
  tests/         Unit tests
```

## Getting Started

```bash
pip install -r requirements.txt
```

## License

MIT
