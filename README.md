# 🎵 Music Recommender Simulation

## Project Summary

SoundMatch 1.0 is a content-based music recommender built in Python. It takes a user's preferred genre, mood, and energy level, scores every song in a 20-track catalog against those preferences, and returns the top 5 most relevant songs with a plain-language explanation for each pick. No machine learning — just weighted math.

---

## How The System Works

**Song features used:**
- `genre` — string label (pop, rock, lofi, etc.)
- `mood` — string label (happy, chill, intense, etc.)
- `mood_tag` — detailed vibe label (euphoric, nostalgic, aggressive, dreamy, melancholic)
- `energy` — float 0.0–1.0, how high-intensity the track feels
- `valence` — float 0.0–1.0, how positive/upbeat the track sounds
- `popularity` — int 0–100, how popular the track is
- `decade` — era of the track (2000s, 2010s, 2020s)
- `tempo_bpm`, `danceability`, `acousticness` — stored, available for future scoring

**User profile stores:**
- `genre` — favorite genre
- `mood` — favorite mood
- `mood_tag` — preferred vibe (e.g. euphoric, nostalgic)
- `energy` — target energy level (0.0–1.0)
- `decade` — preferred era

**How scores are calculated (balanced mode):**

| Signal | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.0 |
| Mood tag match | +0.7 |
| Energy similarity | up to +1.0 |
| Valence similarity | up to +0.5 |
| Popularity bonus | up to +0.3 |
| Decade match | +0.2 |

Songs are ranked highest to lowest. Top 5 are returned with a reasons string explaining which signals fired.

**Scoring modes:**

| Mode | What it prioritizes |
|---|---|
| `balanced` | Even mix of all signals |
| `genre_first` | Genre worth 3.0 — everything else secondary |
| `mood_first` | Mood worth 2.0 — great for vibe-based listening |
| `energy_focused` | Energy worth 2.5 — ignores genre almost entirely |

**Diversity penalty:** max 1 song per artist and max 2 songs per genre in any top-5 result, so the same artist can't dominate the list.

---

## Getting Started

### Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac or Linux
   venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   pip install tabulate
   ```

3. Run the recommender:

   ```bash
   python src/main.py
   ```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

- **4 distinct profiles tested:** Happy Pop Fan (balanced), Chill Lofi Listener (mood_first), High-Energy Rock Head (energy_focused), Nostalgic Jazz Fan (genre_first)
- **Scoring modes:** switching from `balanced` to `energy_focused` caused Storm Runner to jump to #1 for the rock profile with a +2.48 energy score vs +0.98 in balanced mode
- **Diversity penalty:** without it, Voltline took spots #1 and #2 for the rock profile; with it, no artist repeats in any top-5
- **Weight shift:** doubling energy weight caused cross-genre songs to climb higher, producing more surprising but occasionally interesting results
- **Edge case:** a user with `energy: 0.9` and `mood: chill` caused high-energy songs to dominate despite the calm mood preference — energy score outweighed the mood mismatch

---

## Terminal Output

### Happy Pop Fan — balanced mode
```
╭─────┬─────────────────────────────────┬───────────┬──────────┬───────┬───────┬─────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   # │ Song — Artist                   │ Genre     │ Vibe     │ Era   │   Pop │   Score │ Why                                                                                                        │
├─────┼─────────────────────────────────┼───────────┼──────────┼───────┼───────┼─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│   1 │ Sunrise City — Neon Echo        │ pop       │ euphoric │ 2020s │    87 │    5.62 │ genre match (+2.0), mood match (+1.0), mood tag 'euphoric' match (+0.7), energy similarity (+0.98) ...    │
│   2 │ Breakaway — Max Pulse           │ pop       │ euphoric │ 2020s │    90 │    5.60 │ genre match (+2.0), mood match (+1.0), mood tag 'euphoric' match (+0.7), energy similarity (+0.98) ...    │
│   3 │ Electric Dreams — Synthex       │ synthwave │ euphoric │ 2020s │    76 │    3.62 │ mood match (+1.0), mood tag 'euphoric' match (+0.7), energy similarity (+1.00) ...                        │
│   4 │ Rooftop Lights — Indigo Parade  │ indie pop │ euphoric │ 2020s │    83 │    3.60 │ mood match (+1.0), mood tag 'euphoric' match (+0.7), energy similarity (+0.96) ...                        │
│   5 │ Sunday Morning — Paper Lanterns │ indie pop │ euphoric │ 2020s │    80 │    3.35 │ mood match (+1.0), mood tag 'euphoric' match (+0.7), energy similarity (+0.75) ...                        │
╰─────┴─────────────────────────────────┴───────────┴──────────┴───────┴───────┴─────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Chill Lofi Listener — mood_first mode
```
╭─────┬───────────────────────────────┬─────────┬───────────┬───────┬───────┬─────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   # │ Song — Artist                 │ Genre   │ Vibe      │ Era   │   Pop │   Score │ Why                                                                                                        │
├─────┼───────────────────────────────┼─────────┼───────────┼───────┼───────┼─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│   1 │ Library Rain — Paper Lanterns │ lofi    │ nostalgic │ 2020s │    69 │    5.59 │ genre match (+1.0), mood match (+2.0), mood tag 'nostalgic' match (+1.0), energy similarity (+0.80) ...    │
│   2 │ Midnight Coding — LoRoom      │ lofi    │ nostalgic │ 2020s │    74 │    5.55 │ genre match (+1.0), mood match (+2.0), mood tag 'nostalgic' match (+1.0), energy similarity (+0.74) ...    │
│   3 │ Mountain Echo — Cactus Tone   │ country │ nostalgic │ 2010s │    62 │    4.29 │ mood match (+2.0), mood tag 'nostalgic' match (+1.0), energy similarity (+0.78) ...                        │
│   4 │ Deep Blue — Orbit Bloom       │ ambient │ dreamy    │ 2010s │    55 │    3.29 │ mood match (+2.0), energy similarity (+0.70) ...                                                            │
│   5 │ Rainy Cafe — Slow Stereo      │ jazz    │ nostalgic │ 2000s │    60 │    2.29 │ mood tag 'nostalgic' match (+1.0), energy similarity (+0.78) ...                                            │
╰─────┴───────────────────────────────┴─────────┴───────────┴───────┴───────┴─────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### High-Energy Rock Head — energy_focused mode
```
╭─────┬────────────────────────────────┬───────────┬────────────┬───────┬───────┬─────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   # │ Song — Artist                  │ Genre     │ Vibe       │ Era   │   Pop │   Score │ Why                                                                                                        │
├─────┼────────────────────────────────┼───────────┼────────────┼───────┼───────┼─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│   1 │ Storm Runner — Voltline        │ rock      │ aggressive │ 2010s │    81 │    5.20 │ genre match (+1.0), mood match (+0.5), mood tag 'aggressive' match (+0.5), energy similarity (+2.48) ...   │
│   2 │ Gym Hero — Max Pulse           │ pop       │ aggressive │ 2020s │    92 │    4.18 │ mood match (+0.5), mood tag 'aggressive' match (+0.5), energy similarity (+2.48) ...                       │
│   3 │ Neon Jungle — Synthex          │ synthwave │ aggressive │ 2020s │    79 │    3.96 │ mood match (+0.5), mood tag 'aggressive' match (+0.5), energy similarity (+2.40) ...                       │
│   4 │ Sunrise City — Neon Echo       │ pop       │ euphoric   │ 2020s │    87 │    2.97 │ energy similarity (+2.25), valence similarity (+0.46) ...                                                  │
│   5 │ Rooftop Lights — Indigo Parade │ indie pop │ euphoric   │ 2020s │    83 │    2.80 │ energy similarity (+2.10), valence similarity (+0.45) ...                                                  │
╰─────┴────────────────────────────────┴───────────┴────────────┴───────┴───────┴─────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## Limitations and Risks

- Catalog is only 20 songs — way too small for real variety
- Genre matching is exact string comparison, so "indie pop" ≠ "pop"
- System doesn't consider lyrics, language, or cultural context
- Jazz and country only have 2 songs each — genre_first mode collapses to energy/mood fallbacks for those users
- Even with diversity penalty, small catalog means genre bubbles still form

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building SoundMatch made it obvious how much a single weight value shapes every recommendation. The genre weight of +2.0 effectively decides the top results before mood or energy even matter — which is a design choice that embeds a bias whether you intend it or not. Real platforms like Spotify have thousands of signals and feedback loops to balance this out, but even they struggle with filter bubbles. The scary part is how "smart" the results feel even though the system is just doing simple arithmetic — which is a good reminder to always ask *why* an algorithm behaves the way it does, not just whether it works.