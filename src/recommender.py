"""
Music Recommender Simulation - Core Logic

Implements a content-based filtering recommender that scores songs
against a user preference profile using weighted attributes.
"""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score and rank songs for a given UserProfile, returning the top k."""
        # Convert UserProfile to a dict so we can reuse score_song
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        # Convert Song dataclasses to dicts for score_song
        song_dicts = [
            {
                "id": s.id,
                "title": s.title,
                "artist": s.artist,
                "genre": s.genre,
                "mood": s.mood,
                "energy": s.energy,
                "tempo_bpm": s.tempo_bpm,
                "valence": s.valence,
                "danceability": s.danceability,
                "acousticness": s.acousticness,
            }
            for s in self.songs
        ]
        scored = [(song, *score_song(user_prefs, song)) for song in song_dicts]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_dicts = [item[0] for item in scored[:k]]
        # Map back to Song dataclasses
        id_to_song = {s.id: s for s in self.songs}
        return [id_to_song[d["id"]] for d in top_dicts]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
        }
        _, explanation = score_song(user_prefs, song_dict)
        return explanation


# Functional API 
def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields so we can do math on them
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Score a single song against user preferences.

    Scoring rules:
      +2.0  genre match
      +1.0  mood match
      +1.0  energy similarity  (scaled: 1 - |user_energy - song_energy|)
      +0.5  valence similarity (scaled: 1 - |user_energy - song_valence|)
            (valence acts as a proxy for overall positivity)

    Returns:
        (score, explanation_string)
    """
    score = 0.0
    reasons = []

    # Genre match (most important signal) 
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # --- Mood match ---
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    #  Energy similarity (0.0–1.0 scale) 
    if "energy" in user_prefs and "energy" in song:
        energy_gap = abs(user_prefs["energy"] - song["energy"])
        energy_score = round((1.0 - energy_gap) * 1.0, 2)  # max +1.0
        score += energy_score
        reasons.append(f"energy similarity ({energy_score:+.2f})")

    #  Valence similarity (positive-vibe proxy) 
    if "energy" in user_prefs and "valence" in song:
        valence_gap = abs(user_prefs["energy"] - song["valence"])
        valence_score = round((1.0 - valence_gap) * 0.5, 2)  # max +0.5
        score += valence_score
        reasons.append(f"valence similarity ({valence_score:+.2f})")

    explanation = ", ".join(reasons) if reasons else "no strong match"
    return round(score, 2), explanation


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Score every song, then return the top k as (song, score, explanation) tuples.

    Uses sorted() so the original songs list is never mutated.
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    # sorted() returns a new list; .sort() would mutate in place
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]