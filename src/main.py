"""
Command line runner for the Music Recommender Simulation.
Tests three distinct user profiles to evaluate recommender behavior.
"""

from recommender import load_songs, recommend_songs


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a labeled, formatted block of recommendations."""
    print(f"\n{'='*50}")
    print(f"  🎵  {label}")
    print(f"{'='*50}")
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    #  Profile 1: Happy Pop Fan 
    pop_prefs = {"genre": "pop", "mood": "happy", "energy": 0.80}
    pop_recs = recommend_songs(pop_prefs, songs, k=5)
    print_recommendations("Happy Pop Fan", pop_recs)

    #  Profile 2: Chill Lofi Listener 
    lofi_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    lofi_recs = recommend_songs(lofi_prefs, songs, k=5)
    print_recommendations("Chill Lofi Listener", lofi_recs)

    #  Profile 3: High-Energy Rock Head 
    rock_prefs = {"genre": "rock", "mood": "intense", "energy": 0.92}
    rock_recs = recommend_songs(rock_prefs, songs, k=5)
    print_recommendations("High-Energy Rock Head", rock_recs)


if __name__ == "__main__":
    main()