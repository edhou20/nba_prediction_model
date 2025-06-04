from data import scrape_player_stats, scrape_team_stats, get_soup


if __name__ == "__main__":
    # Change the season here — 2025 season = 2024–25
    print("in main")
    season_year = 2025

    player_df = scrape_player_stats(season_year)
    team_df = scrape_team_stats(season_year)

    print("Sample player data:\n", player_df.head())
    print("Sample team data:\n", team_df.head())

    # Save to CSV
    player_df.to_csv(f"players_{season_year}.csv", index=False)
    team_df.to_csv(f"teams_{season_year}.csv", index=False)
    print("Data saved")