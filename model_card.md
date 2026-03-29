# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**SoundMatch 1.0**

---

## 2. Intended Use

Suggests songs based on a user's favorite genre, mood, energy level, preferred vibe, and era. Built for a classroom simulation — not for real users. Assumes the user can be described by a handful of preferences, which is obviously a simplification.

---

## 3. How the Model Works

Every song gets a score. Genre match adds the most points, then mood, then a detailed vibe tag (like "euphoric" or "nostalgic"), then how close the song's energy is to what the user wants. Valence, popularity, and era add smaller bonuses. Songs are ranked by score and the top 5 are returned with a short reason explaining what matched.

You can also switch scoring modes: genre_first makes genre worth 3x, mood_first doubles the mood weight, energy_focused makes energy the dominant signal. A diversity penalty prevents the same artist or genre from taking over the whole list.

No machine learning. Just weighted math with a few knobs to turn.

---

## 4. Data

20 songs in a CSV. Genres include pop, lofi, rock, synthwave, jazz, ambient, indie pop, r&b, and country. Mood tags include euphoric, nostalgic, aggressive, dreamy, and melancholic. Decades span 2000s–2020s. Pop and lofi are still overrepresented. No hip-hop, classical, metal, or anything non-Western. Added 10 songs to the original 10 to get more variety, plus new columns for mood_tag, popularity, and decade.

---

## 5. Strengths

- Works well when the user's genre is in the catalog — top results feel genuinely relevant
- Mood tags add a layer of nuance that plain mood labels miss (aggressive vs intense isn't the same thing)
- Scoring modes make the system flexible — energy_focused actually produces interesting cross-genre surprises
- Diversity penalty meaningfully changes results — without it Voltline took the top 2 rock spots every time
- Explanation strings are readable and specific enough to be useful

---

## 6. Limitations and Bias

- Genre weight still dominates in balanced mode even with the new signals
- Jazz and country only have 2 songs each — genre_first mode for those users just falls back to energy/mood guesswork
- Exact string matching still means "indie pop" ≠ "pop"
- Popularity bonus slightly favors well-known tracks regardless of fit — a 92-popularity song that doesn't match anything still gets a small boost
- Decade matching is binary — 2019 and 2021 are different decades even though they sound the same

---

## 7. Evaluation

Tested four profiles: Happy Pop Fan (balanced), Chill Lofi Listener (mood_first), High-Energy Rock Head (energy_focused), Nostalgic Jazz Fan (genre_first). Top 2 results for pop, lofi, and rock all felt right. Jazz Fan was the weakest — only 2 jazz songs in the catalog so results 3–5 were basically random energy matches. Diversity penalty test: disabled it for rock and Voltline immediately took #1 and #2. Confirmed the penalty works. Switching rock to energy_focused pushed Storm Runner's score from 4.27 to 5.20 — the mode difference is real and measurable.

---

## 8. Future Work

- Fuzzy genre matching so "indie pop" partially counts as "pop"
- Separate user valence preference instead of using energy as a proxy
- Expand the catalog — especially underrepresented genres
- User feedback loop: if a song gets skipped, reduce the weight of whichever signal matched it

---

## 9. Personal Reflection

Adding scoring modes was the most interesting part — it made the bias visible in a concrete way. In energy_focused mode, genre basically stops mattering and songs from completely different genres float to the top just because they hit the right BPM range. That's not wrong, it's just a different opinion about what music taste means. The diversity penalty also felt important — without it the system confidently recommends the same artist twice and calls it variety. Real recommenders probably have a hundred versions of that same fix running in parallel.