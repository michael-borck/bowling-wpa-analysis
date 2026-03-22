# Connection Between the Two Papers

## Paper 1: Skill, Sequence, and Scoring (current — submitted to JQAS)

**Repository:** [github.com/michael-borck/skill-sequence-scoring](https://github.com/michael-borck/skill-sequence-scoring)

## Paper 2: Win Probability and Leverage (next)

**Repository:** [github.com/michael-borck/bowling-wpa-analysis](https://github.com/michael-borck/bowling-wpa-analysis)

---

## Side-by-Side Comparison

| | Paper 1 (Scoring) | Paper 2 (WPA) |
|---|---|---|
| **Question** | What does each system *measure* about a player's performance? | How does each system affect *competitive dynamics* between two players in a live match? |
| **Unit of analysis** | Single complete game | Head-to-head match in progress |
| **Methods** | Exact combinatorial enumeration + Monte Carlo simulation | Win probability computation at every game state + leverage index |
| **Core finding** | Traditional scoring encodes sequence + pin count; World Bowling encodes only pin count | (Expected) Traditional scoring creates more high-leverage frames — more dramatic competitive swings |
| **Key metric** | Score standard deviation, sequence sensitivity | Win Probability Added (WPA), leverage index |
| **Crossover result** | ~50% strike rate: below this WB is fine, above it traditional is superior | (Expected) Leverage differential grows with skill level, mirroring the crossover |
| **Answers the question** | "Is anything lost when scoring is simplified?" | "Does it matter for competition?" |
| **Broadcast relevance** | Indirect — score spread implies competitive consequences | Direct — traditional scoring creates more dramatic TV moments, not fewer |
| **Relationship** | Foundation | Extension — cites Paper 1 as the measurement basis |

## Why Two Papers, Not One

- **Different questions** require different methods. Paper 1 is about measurement instruments. Paper 2 is about game theory and competition dynamics.
- **Different audiences within JQAS.** Paper 1 appeals to combinatorics and sports science readers. Paper 2 appeals to competition design and broadcast analytics readers.
- **Stronger together.** Paper 1 proves *what* is lost. Paper 2 proves *why it matters in a match*. Each is complete on its own but cites the other.
- **Manageable scope.** Combining both would double the length and dilute both arguments.

## The Narrative Arc

```
Paper 1: "Traditional scoring measures more about a player's skill."
     ↓
Paper 2: "And that measurement creates better competition."
     ↓
Combined implication: "Simplifying the scoring system doesn't just
lose information — it makes matches less competitive and less dramatic."
```

## Key References Shared Between Papers

- Cooper & Kennedy (1990) — foundational score distributions
- VanDerwerken & Kenter (2018) — Markov bowling model (published in JQAS)
- Yaari & Eisenmann (2012) — hot hand in bowling, PBA data
- Borck (2026) — Paper 1 (cited by Paper 2)
