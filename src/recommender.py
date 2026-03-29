"""
Music Recommender Simulation - Core Logic

Implements a content-based filtering recommender with:
  - Challenge 1: Advanced features (popularity, decade, mood_tag)
  - Challenge 2: Multiple scoring modes (genre-first, mood-first, energy-focused)
  - Challenge 3: Diversity penalty (no artist/genre domination)
  - Challenge 4: Tabulate-powered terminal output (handled in main.py)
"""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


# 
# Data classes
# 

@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    mood_tag: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int
    decade: str


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper around the functional API. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k Song dataclasses for a UserProfile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dicts = [_song_to_dict(s) for s in self.songs]
        results = recommend_songs(user_prefs, song_dicts, k=k)
        id_to_song = {s.id: s for s in self.songs}
        return [id_to_song[r[0]["id"]] for r in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Plain-language explanation for a single song recommendation."""
        user_prefs = {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}
        _, explanation = score_song(user_prefs, _song_to_dict(song))
        return explanation


def _song_to_dict(s: Song) -> Dict:
    """Convert a Song dataclass to a plain dict."""
    return {
        "id": s.id, "title": s.title, "artist": s.artist,
        "genre": s.genre, "mood": s.mood, "mood_tag": s.mood_tag,
        "energy": s.energy, "tempo_bpm": s.tempo_bpm, "valence": s.valence,
        "danceability": s.danceability, "acousticness": s.acousticness,
        "popularity": s.popularity, "decade": s.decade,
    }


# 
# Challenge 2: Scoring modes (Strategy pattern)
# 

SCORING_MODES = {
    "genre_first":     {"genre": 3.0, "mood": 0.5, "energy": 0.5, "mood_tag": 0.5, "popularity": 0.3, "decade": 0.2},
    "mood_first":      {"genre": 1.0, "mood": 2.0, "energy": 0.8, "mood_tag": 1.0, "popularity": 0.3, "decade": 0.2},
    "energy_focused":  {"genre": 1.0, "mood": 0.5, "energy": 2.5, "mood_tag": 0.5, "popularity": 0.3, "decade": 0.2},
    "balanced":        {"genre": 2.0, "mood": 1.0, "energy": 1.0, "mood_tag": 0.7, "popularity": 0.3, "decade": 0.2},
}


# 
# Functional API
# 

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of typed dicts."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"]   = int(row["popularity"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    mode: str = "balanced",
) -> Tuple[float, str]:
    """
    Score a single song against user preferences using the given mode.

    Challenge 1 signals:
      - mood_tag match    (e.g. euphoric, nostalgic, aggressive)
      - popularity bonus  (scaled 0–1 from 0–100)
      - decade match      (bonus if song decade == user preferred decade)

    Challenge 2: weights come from SCORING_MODES dict.

    Returns:
        (score, explanation_string)
    """
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons = []

    #  Genre match 
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts:.1f})")

    #  Mood match 
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts:.1f})")

    #  Mood tag match (Challenge 1) 
    if user_prefs.get("mood_tag") and song.get("mood_tag", "").lower() == user_prefs["mood_tag"].lower():
        pts = weights["mood_tag"]
        score += pts
        reasons.append(f"mood tag '{song['mood_tag']}' match (+{pts:.1f})")

    #  Energy similarity 
    if "energy" in user_prefs and "energy" in song:
        energy_score = round((1.0 - abs(user_prefs["energy"] - song["energy"])) * weights["energy"], 2)
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score:.2f})")

    #  Valence similarity 
    if "energy" in user_prefs and "valence" in song:
        valence_score = round((1.0 - abs(user_prefs["energy"] - song["valence"])) * 0.5, 2)
        score += valence_score
        reasons.append(f"valence similarity (+{valence_score:.2f})")

    #  Popularity bonus (Challenge 1): scaled 0.0–max 0.3 
    if "popularity" in song:
        pop_score = round((song["popularity"] / 100) * weights["popularity"], 2)
        score += pop_score
        reasons.append(f"popularity bonus (+{pop_score:.2f})")

    #  Decade match (Challenge 1) 
    if user_prefs.get("decade") and song.get("decade") == user_prefs["decade"]:
        pts = weights["decade"]
        score += pts
        reasons.append(f"decade match {song['decade']} (+{pts:.1f})")

    explanation = ", ".join(reasons) if reasons else "no strong match"
    return round(score, 2), explanation


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: bool = True,
) -> List[Tuple[Dict, float, str]]:
    """
    Score every song, apply optional diversity penalty, return top-k.

    Challenge 2: pass mode="genre_first" / "mood_first" / "energy_focused"
    Challenge 3: diversity_penalty=True prevents same artist/genre dominating
    """
    # Score every song
    scored = [(song, *score_song(user_prefs, song, mode=mode)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    if not diversity_penalty:
        return ranked[:k]

    #  Challenge 3: Diversity penalty 
    # Allow max 1 song per artist, max 2 per genre in the final top-k
    results = []
    artist_count: Dict[str, int] = {}
    genre_count: Dict[str, int] = {}

    for song, score, explanation in ranked:
        artist = song["artist"]
        genre  = song["genre"]

        if artist_count.get(artist, 0) >= 1:
            continue  # already have this artist
        if genre_count.get(genre, 0) >= 2:
            continue  # already have 2 of this genre

        results.append((song, score, explanation))
        artist_count[artist] = artist_count.get(artist, 0) + 1
        genre_count[genre]   = genre_count.get(genre, 0) + 1

        if len(results) == k:
            break

    return results