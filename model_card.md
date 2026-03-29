# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**SoundMatch 1.0**

---

## 2. Intended Use

Suggests songs based on a user's favorite genre, mood, and energy level. Built for a classroom simulation — not for real users. Assumes the user can be described by just three preferences, which is obviously a simplification.

---

## 3. How the Model Works

Every song in the catalog gets a score. A genre match adds the most points, then mood, then how close the song's energy is to what the user wants. Valence (how positive a song feels) adds a small bonus. Songs are ranked by score and the top 5 are returned with a short reason explaining what matched.

No machine learning. Just weighted math.

---

## 4. Data

20 songs in a CSV file. Genres include pop, lofi, rock, synthwave, jazz, ambient, indie pop, r&b, and country. Moods include happy, chill, intense, relaxed, moody, and focused. Pop and lofi are overrepresented. No hip-hop, classical, metal, or anything non-Western. Added 10 songs to the original 10 to get more variety.

---

## 5. Strengths

- Works well when the user's genre is in the catalog — top results feel genuinely relevant
- The explanation strings ("genre match, mood match") make it easy to understand why something was recommended
- Energy similarity does a decent job of separating chill songs from hype songs even across genres

---

## 6. Limitations and Bias

- Genre weight is too strong — a genre match almost always wins regardless of everything else
- Exact string matching means "indie pop" and "pop" are treated as completely different
- Small dataset means the same artists keep showing up
- High-energy songs bleed into profiles they don't belong in
- No consideration of tempo, danceability, or acousticness in the scoring

---

## 7. Evaluation

Tested three profiles: Happy Pop Fan, Chill Lofi Listener, High-Energy Rock Head. Top 2 results for each profile made sense. Gym Hero showed up for both pop and rock users because of its high energy — that was unexpected. Temporarily removing the mood check shuffled the rankings a lot, which confirmed mood is the second most important signal after genre.

---

## 8. Future Work

- Fuzzy genre matching so "indie pop" partially counts as "pop"
- Diversity penalty to stop the same artist appearing multiple times
- Add user feedback — if a song gets skipped, lower the weight of whatever signal matched it

---

## 9. Personal Reflection

Learned that recommendation systems are basically just ranked math with opinions baked into the weights. The surprising part was how "smart" it feels even though it's just addition. Also made me realize how much Spotify probably knows about me if this toy version can already narrow things down with three inputs.