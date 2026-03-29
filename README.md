# 🎵 Music Recommender Simulation

## Project Summary

SoundMatch 1.0 is a content-based music recommender built in Python. It takes a user's preferred genre, mood, and energy level, scores every song in a 20-track catalog against those preferences, and returns the top 5 most relevant songs with a plain-language explanation for each pick. No machine learning — just weighted math.

---

## How The System Works

**Song features used:**
- `genre` — string label (pop, rock, lofi, etc.)
- `mood` — string label (happy, chill, intense, etc.)
- `energy` — float 0.0–1.0, how high-intensity the track feels
- `valence` — float 0.0–1.0, how positive/upbeat the track sounds
- `tempo_bpm`, `danceability`, `acousticness` — stored but available for future scoring

**User profile stores:**
- `genre` — favorite genre
- `mood` — favorite mood
- `energy` — target energy level (0.0–1.0)

**How scores are calculated:**

| Signal | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.0 |
| Energy similarity | up to +1.0 |
| Valence similarity | up to +0.5 |

Songs are ranked highest to lowest. Top 5 are returned with a reasons string explaining which signals fired.

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

- **3 distinct profiles tested:** Happy Pop Fan, Chill Lofi Listener, High-Energy Rock Head — all returned sensible top-2 results matching both genre and mood.
- **Weight shift:** Doubling energy weight caused cross-genre songs to climb higher, producing more surprising results.
- **Feature removal:** Commenting out the mood check shifted rankings noticeably, confirming mood is the second most influential signal after genre.
- **Edge case:** A user with `energy: 0.9` and `mood: chill` caused high-energy songs to dominate despite the calm mood preference — the energy score outweighed the mood mismatch.

---

## Terminal Output Screenshots

### Happy Pop Fan
```
==================================================
  🎵  Happy Pop Fan
==================================================
  1. Sunrise City by Neon Echo
     Score : 4.46
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.98), valence similarity (+0.48)

  2. Breakaway by Max Pulse
     Score : 4.43
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.98), valence similarity (+0.45)

  3. Gym Hero by Max Pulse
     Score : 3.35
     Why   : genre match (+2.0), energy similarity (+0.87), valence similarity (+0.48)

  4. Electric Dreams by Synthex
     Score : 2.49
     Why   : mood match (+1.0), energy similarity (+1.00), valence similarity (+0.49)

  5. Rooftop Lights by Indigo Parade
     Score : 2.45
     Why   : mood match (+1.0), energy similarity (+0.96), valence similarity (+0.49)
```

### Chill Lofi Listener
```
==================================================
  🎵  Chill Lofi Listener
==================================================
  1. Library Rain by Paper Lanterns
     Score : 4.38
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.00), valence similarity (+0.38)

  2. Midnight Coding by LoRoom
     Score : 4.32
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.93), valence similarity (+0.39)

  3. Focus Flow by LoRoom
     Score : 3.33
     Why   : genre match (+2.0), energy similarity (+0.95), valence similarity (+0.38)

  4. Deep Blue by Orbit Bloom
     Score : 2.29
     Why   : mood match (+1.0), energy similarity (+0.87), valence similarity (+0.42)

  5. Mountain Echo by Cactus Tone
     Score : 2.29
     Why   : mood match (+1.0), energy similarity (+0.97), valence similarity (+0.32)
```

### High-Energy Rock Head
```
==================================================
  🎵  High-Energy Rock Head
==================================================
  1. Storm Runner by Voltline
     Score : 4.27
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.99), valence similarity (+0.28)

  2. Thunder Anthem by Voltline
     Score : 4.24
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.97), valence similarity (+0.27)

  3. Gym Hero by Max Pulse
     Score : 2.41
     Why   : mood match (+1.0), energy similarity (+0.99), valence similarity (+0.42)

  4. Neon Jungle by Synthex
     Score : 2.28
     Why   : mood match (+1.0), energy similarity (+0.96), valence similarity (+0.32)

  5. Sunrise City by Neon Echo
     Score : 1.36
     Why   : energy similarity (+0.90), valence similarity (+0.46)
```

---

## Limitations and Risks

- Catalog is only 20 songs — way too small for real variety
- Genre matching is exact string comparison, so "indie pop" ≠ "pop"
- System doesn't consider lyrics, language, or cultural context
- Genre weight (+2.0) dominates everything — great mood/energy matches from other genres rarely surface
- Same artists appear repeatedly because the dataset is small

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building SoundMatch made it obvious how much a single weight value shapes every recommendation. The genre weight of +2.0 effectively decides the top results before mood or energy even matter — which is a design choice that embeds a bias whether you intend it or not. Real platforms like Spotify have thousands of signals and feedback loops to balance this out, but even they struggle with filter bubbles. The scary part is how "smart" the results feel even though the system is just doing simple arithmetic — which is a good reminder to always ask *why* an algorithm behaves the way it does, not just whether it works.