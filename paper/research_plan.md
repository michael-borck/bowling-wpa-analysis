# Research Plan

## Title

"Win Probability and Leverage: How Scoring System Design Shapes Competitive Dynamics in Ten-Pin Bowling"

## Core Research Question

How does each scoring system (traditional vs. World Bowling) affect the probability of winning a head-to-head match at each game state? Does traditional scoring create more "high-leverage" moments — frames where a single ball dramatically shifts the match outcome?

## Connection to the Scoring Paper

This paper is a direct follow-up to Borck (2026), "Skill, Sequence, and Scoring: A Mathematical Argument for Traditional Ten-Pin Bowling Scoring." That paper established three key results:

1. Traditional scoring is **sequence-sensitive** — the order of strikes and spares matters, rewarding sustained performance streaks.
2. Traditional scoring has a **compounding reward gradient** — each consecutive strike is worth more than the last.
3. Traditional scoring has **higher Shannon entropy** — it spreads scores across a wider range, better discriminating between skill levels.

The scoring paper deliberately left one question open: how does scoring system design affect **head-to-head competition dynamics**? This paper answers that question by introducing Win Probability Added (WPA) and Leverage Index analysis to bowling.

The central thesis: traditional scoring's sequence sensitivity and compounding bonuses don't just measure skill better — they create **more dramatic competitive moments** in live matches. The cross-frame dependencies that critics call "confusing" are exactly what generate the high-leverage situations that make bowling exciting to watch and compete in.

## Methodology

### 1. Win Probability Engine

For any game state `(frame, ball, score_A, score_B, pending_bonuses_A, pending_bonuses_B)` under both scoring systems, compute `P(player A wins)`.

**Approach:**
- **Monte Carlo method (primary):** From the current state, simulate the remainder of the game N times using the Markov chain model from the scoring paper. P(A wins) = fraction of simulations where A's final score > B's final score.
- **Exact DP method (World Bowling only):** Because World Bowling has no cross-frame bonuses, the state space is smaller and exact computation via dynamic programming is feasible. Use this as a validation benchmark.
- **Calibration:** Use the same skill tiers and Markov transition probabilities established in the scoring paper (Table 2 / simulation parameters).

**Key implementation detail:** Traditional scoring requires tracking pending bonuses (unresolved strikes/spares), making the state space much larger. This is itself an interesting result — the richer state space is what generates more varied leverage profiles.

### 2. Win Probability Added (WPA)

For each ball thrown in a match:

```
WPA = P(A wins | after ball) - P(A wins | before ball)
```

A strike in frame 7 when trailing by 15 pins has a very different WPA than a strike in frame 2 of a blowout. WPA captures the **contextual importance** of each ball.

### 3. Leverage Index (LI)

```
LI = E[|WPA|] for the next ball
```

Normalised so that the average LI across all balls in a game equals 1.0. High LI means the next ball will have an outsized impact on the match outcome.

**Hypothesis:** Traditional scoring produces higher peak leverage and higher leverage variance because:
- Cross-frame bonuses mean a strike in frame 9 affects the score of frames 7, 8, AND 9
- The compounding effect creates "double jeopardy" moments where a miss costs both the current frame and the bonus from a previous frame
- Late-game leverage is amplified because unresolved bonuses create score uncertainty

### 4. Leverage Profile Analysis

For each scoring system, compute the average leverage index at each frame position across thousands of simulated matches between equal-skill opponents.

**Expected result:** Traditional scoring shows a characteristic "rising leverage" profile — leverage increases through the game as cross-frame dependencies accumulate and the score margin narrows. World Bowling shows a flatter profile because each frame is self-contained.

### 5. Clutch Moment Analysis

Define a "clutch moment" as any ball where the leverage index exceeds the 90th percentile. Compare:
- Frequency of clutch moments per match under each system
- Distribution of clutch moment magnitude (how much can a single ball swing?)
- Frame distribution of clutch moments (where do they cluster?)
- "Delivery rate" under pressure — how often do players convert in clutch moments?

### 6. Outcome Concordance: How Often Do the Systems Agree?

Take completed game sequences (simulated or, if available, actual PBA data) and score each under both systems. For head-to-head matches, ask:

- **Overall concordance:** In what percentage of games does the same player win under both systems?
- **By margin:** Break down by traditional score margin. Blowouts (>30 pts) should show near-100% concordance. Close games (<10 pts) should show significant divergence.
- **By skill tier:** At recreational level, concordance should be very high. At professional level, lower.
- **Tournament impact:** Over a season or tournament series, does the *ranking* of players change? Does the *champion* change?

**Why this matters:** A representative of the Asian Bowling Federation has claimed publicly that re-scoring historical games under current-frame rules produces the same winners. This is likely true for most games — but the critical question is whether it holds for *close games between elite players*, which are exactly the games that decide tournaments. Even a 10% outcome divergence in close professional matches would represent a meaningful change in competitive outcomes.

**Prediction:** Overall concordance will be >90%, but concordance in games decided by fewer than 10 traditional-scoring points will drop to 75-85%. This is the key finding — the systems usually agree, but they disagree precisely when it matters most.

### 7. The Broadcast Argument

Connect leverage analysis to the debate about bowling's television appeal:
- Traditional scoring creates MORE dramatic moments, not fewer
- The "confusing" cross-frame bonuses are precisely what generates the tension ("Can she close with a strike to lock out the bonus?")
- World Bowling's frame independence eliminates the cascading drama
- Quantify: how many fewer "swing moments" does a typical World Bowling match have?

## Key Analyses to Implement

1. **WPA engine validation:** Compare Monte Carlo WP estimates against exact DP for World Bowling; verify convergence.
2. **Single-match WPA curves:** Plot P(A wins) through a complete match under both systems. Show how traditional scoring creates wider swings.
3. **Leverage by frame:** Average LI at each frame position. Show traditional scoring's rising-leverage characteristic.
4. **Leverage distribution:** Histogram of all LI values across many matches. Show traditional has heavier tails.
5. **Clutch frequency comparison:** Count clutch moments per match under each system.
6. **Skill-dependent leverage:** How does leverage profile change across skill tiers? (Higher-skill matches should have higher leverage in traditional because strikes and spares create larger bonuses.)
7. **Strike-in-context analysis:** WPA of a strike at each frame position. Show that traditional scoring makes late-game strikes dramatically more valuable.

## Figures for the Paper

### Figure 1: Win Probability Curves — Sample Match
Two panels (traditional / World Bowling) showing P(A wins) through a complete match between equal-skill opponents. Same ball sequence in both panels. Traditional panel should show wider swings and more dramatic shifts.

### Figure 2: Leverage Index by Frame
Line plot with error bands showing mean LI at each frame (1–10) under both systems. Traditional should show rising leverage; World Bowling should be flatter.

### Figure 3: Leverage Distribution
Overlaid histograms (or KDE) of LI across all balls in N matches. Traditional should have heavier right tail (more extreme leverage moments).

### Figure 4: Clutch Moment Frequency
Bar chart comparing clutch moments per match under each system, broken down by frame. Traditional should show more clutch moments overall, concentrated in frames 8–10.

### Figure 5: Strike WPA by Frame
Heatmap or line plot showing the WPA of a strike at each frame position, for various score differentials. Traditional should show dramatically higher WPA for late-game strikes.

### Figure 6: Leverage Across Skill Tiers
Faceted plot showing leverage profiles for Recreational, Competitive, and Professional tiers. Shows how the leverage difference between systems is amplified at higher skill levels.

### Figure 7: Outcome Concordance by Score Margin
Left: overall concordance rate (% of games where same player wins under both systems), by skill tier. Right: concordance as a function of traditional score margin — showing that the systems diverge most in close games.

## Key References

1. **Borck, M. (2026).** "Skill, Sequence, and Scoring: A Mathematical Argument for Traditional Ten-Pin Bowling Scoring." *Journal of Quantitative Analysis in Sports* (submitted). — Foundation for scoring functions and Markov simulation model.

2. **VanDerwerken, D. N. & Kenter, F. H. J. (2018).** "A Markov Chain Analysis of Bowling." *Journal of Quantitative Analysis in Sports*, 14(1), 1–13. — Markov chain model for bowling; transition probabilities calibrated from PBA data.

3. **Tango, T. M., Lichtman, M. G., & Dolphin, A. E. (2007).** *The Book: Playing the Percentages in Baseball.* Potomac Books. — Original Leverage Index methodology.

4. **FanGraphs.** "Win Probability Added (WPA)." FanGraphs Library. — Standard WPA methodology adapted from baseball.

5. **Yaari, G. & Eisenmann, S. (2012).** "The Hot (Invisible?) Hand: Can Statistical Tests Detect Streakiness?" *The American Statistician*, 66(1), 3–4. — Evidence for sequential dependence in bowling.

6. **Keogh, C. & O'Neill, S. (2011).** "Spare conversion rates in ten-pin bowling." — Spare difficulty class data used in simulation model.

## Target Journal

*Journal of Quantitative Analysis in Sports* (De Gruyter) — same as the scoring paper. The WPA/leverage framework should appeal to the same readership and provides a natural companion piece.

## Timeline

1. **Phase 1 — WPA Engine** (2 weeks): Implement Monte Carlo WP computation, validate against exact DP for World Bowling.
2. **Phase 2 — Match Simulation** (1 week): Simulate head-to-head matches with WPA/LI tracking.
3. **Phase 3 — Analysis** (2 weeks): Generate leverage profiles, clutch analysis, and all figures.
4. **Phase 4 — Writing** (2 weeks): Draft manuscript, focusing on the narrative that scoring system design shapes competitive drama.
5. **Phase 5 — Revision** (1 week): Polish, peer feedback, submit.

## Paper Outline

1. **Introduction:** Bowling scoring reform debate; gap in understanding competitive dynamics. Frame within the broader pattern of sports simplifying scoring for broadcast — badminton's shift to rally scoring (2006), table tennis's reduction to 11-point games (2001), cricket's proliferation of shorter formats. In each case the same tension arises: broadcast pacing vs competitive discrimination. Bowling's finite combinatorics makes it uniquely tractable for formal analysis of what is lost. Note that bowling's most commercially successful broadcast era (ABC Pro Bowlers Tour, 1962-1997, 36 seasons) used traditional scoring exclusively — scoring complexity per se has not historically been a barrier to television appeal.
2. **Background:** Scoring systems (brief, citing scoring paper); WPA/LI concepts from baseball.
3. **Model:** Game state representation; WP computation; LI definition; simulation setup.
4. **Results:**
   - 4.1 Win probability curves under both systems
   - 4.2 Leverage profiles by frame
   - 4.3 Leverage distributions
   - 4.4 Clutch moment analysis
   - 4.5 Skill-tier dependence
   - 4.6 Outcome concordance — how often do the systems agree on the winner?
5. **Discussion:** Traditional scoring creates more dramatic competition; outcome concordance shows systems agree on most results but diverge where it matters most; implications for the reform debate; the broadcast argument.
6. **Conclusion:** Scoring system design is not just about measurement — it shapes the competitive experience.
