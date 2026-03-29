"""
Music Recommender Simulation - CLI Runner

Demonstrates all 4 optional challenges:
  - Challenge 1: Advanced features (mood_tag, popularity, decade)
  - Challenge 2: Multiple scoring modes
  - Challenge 3: Diversity penalty
  - Challenge 4: Tabulate formatted output
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def print_recommendations(label: str, recommendations: list, mode: str) -> None:
    """Print a labeled, tabulate-formatted recommendation block."""
    print(f"\n{'='*70}")
    print(f"  🎵  {label}  |  mode: {mode}")
    print(f"{'='*70}")

    if HAS_TABULATE:
        rows = []
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            rows.append([
                i,
                f"{song['title']} — {song['artist']}",
                song['genre'],
                song['mood_tag'],
                song['decade'],
                song['popularity'],
                f"{score:.2f}",
                explanation,
            ])
        headers = ["#", "Song — Artist", "Genre", "Vibe", "Era", "Pop", "Score", "Why"]
        print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))
    else:
        # Fallback ASCII table if tabulate not installed
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"  {i}. {song['title']} by {song['artist']}")
            print(f"     Genre : {song['genre']}  |  Vibe: {song['mood_tag']}  |  Era: {song['decade']}  |  Pop: {song['popularity']}")
            print(f"     Score : {score:.2f}")
            print(f"     Why   : {explanation}")
            print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    #  Profile 1: Happy Pop Fan — balanced mode 
    pop_prefs = {
        "genre": "pop", "mood": "happy", "mood_tag": "euphoric",
        "energy": 0.80, "decade": "2020s"
    }
    pop_recs = recommend_songs(pop_prefs, songs, k=5, mode="balanced", diversity_penalty=True)
    print_recommendations("Happy Pop Fan", pop_recs, mode="balanced")

    #  Profile 2: Chill Lofi Listener — mood-first mode 
    lofi_prefs = {
        "genre": "lofi", "mood": "chill", "mood_tag": "nostalgic",
        "energy": 0.35, "decade": "2020s"
    }
    lofi_recs = recommend_songs(lofi_prefs, songs, k=5, mode="mood_first", diversity_penalty=True)
    print_recommendations("Chill Lofi Listener", lofi_recs, mode="mood_first")

    #  Profile 3: High-Energy Rock Head — energy-focused mode 
    rock_prefs = {
        "genre": "rock", "mood": "intense", "mood_tag": "aggressive",
        "energy": 0.92, "decade": "2010s"
    }
    rock_recs = recommend_songs(rock_prefs, songs, k=5, mode="energy_focused", diversity_penalty=True)
    print_recommendations("High-Energy Rock Head", rock_recs, mode="energy_focused")

    #  Profile 4: Nostalgic Jazz Fan — genre-first mode 
    jazz_prefs = {
        "genre": "jazz", "mood": "relaxed", "mood_tag": "nostalgic",
        "energy": 0.36, "decade": "2000s"
    }
    jazz_recs = recommend_songs(jazz_prefs, songs, k=5, mode="genre_first", diversity_penalty=True)
    print_recommendations("Nostalgic Jazz Fan", jazz_recs, mode="genre_first")


if __name__ == "__main__":
    main()