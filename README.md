V1: projects the likelihood (in %) of which of 2 teams in the 2024-25 NBA season would win the game, based on historical data from the past 3 seasons

historical data includes:

- player_stats, season-team-player keys
- team_stats, team-season keys
- games, date-team1-team2-target (1 if team1 wins, 0 if team2 wins)

We condense each team-season's players' stats into aggregates (e.g. avgs) and merge them with the existing season-team stats Then we create a diff_df that vectorizes each game We train on 80%, then fit a classifier model to the other 20% We output a percentage of which team wins of the 2 user inputs Evaluate by eyeball test applying domain knowledge of 2024-25 NBA season

Scripts:
- data fetch
- preprocessing
- model script
- evaluation/visualization/UI apps TBD
- UI for injuries on/off
