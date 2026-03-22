# McCarthy (2011) — Notes for Paper 2

**Full citation:** McCarthy, D. (2011). Estimating Different Sources of Variation and Predicting Tournament Outcomes in Professional Bowling. *CHANCE*, 24(3), 37-46. DOI: 10.1080/09332480.2011.10739873

## Key data

- 278,579 PBA National Tour games from 3,931 bowlers
- 117 tournaments, 2004–2010 seasons
- PBA mean score: 205.65, SD: 31.91
- Bowler ability estimates range from ~150 to ~235
- 555 perfect games (300) in the dataset
- Data scraped from PBA.com and bowlingdigital.com

## Bayesian hierarchical model

McCarthy separates three sources of variation:

```
μ_ij = θ_i + γ_j
y_ij ~ Normal(μ_ij, σ)
```

Where:
- θ_i = intrinsic ability of bowler i (average score in an average tournament)
- γ_j = difficulty of tournament j (deviation from average)
- σ = residual game-to-game noise

This decomposition is directly useful for Paper 2.

## How to use in Paper 2

### 1. Better WPA computation
Incorporate tournament difficulty as a parameter. A player who's 5 points
better on average wins less often on a hard oil pattern (where variance
compresses) than on an easy one. Simulate matches at varying difficulty
levels, not just fixed skill tiers.

### 2. Outcome concordance
When re-scoring games under both systems and asking "does the winner
change?", separate genuine close matches from matches that only look
close because of tournament difficulty. Two bowlers scoring 210 and 208
on a hard pattern are more closely matched than the same scores on an
easy pattern.

### 3. Implementation approach
Don't implement the full Bayesian machinery (overkill for our question).
Instead, borrow the insight: add a tournament difficulty parameter that
shifts both players' means. Show traditional scoring's advantage holds
across varying difficulty levels. Maybe 20 lines of code on top of
existing simulation.

## Other useful observations from the paper

- The multimodal score distribution (peaks at 10-point intervals) is
  because elite bowlers knock down either 9 or 10 pins on first ball
- When scores are binned into 10-point intervals, the distribution
  becomes approximately normal (slight positive skew, negative kurtosis)
- Tournament difficulty (oil pattern) is the biggest environmental factor
- Professional bowlers often have other jobs, limiting games played;
  the very best bowl the most games (selection effect worth noting)

## Data request

Draft email to McCarthy is in the Paper 1 repo at:
skill-sequence-scoring/references/mccarthy_email_draft.md

Also request data from:
- VanDerwerken (26K games, ball-by-ball, 2003-2014)
- PBA directly (current data, via Tackett/Belmonte)
