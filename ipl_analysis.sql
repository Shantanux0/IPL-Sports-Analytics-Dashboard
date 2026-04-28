-- ==============================================================================
-- IPL Sports Analytics - Comprehensive SQL Analysis
-- ==============================================================================
-- Note: This script assumes two main tables: 'matches' and 'deliveries'.
-- You can run these queries on PostgreSQL, MySQL, or SQL Server.

-- ==============================================================================
-- 1. Top Performing Batsmen (Runs & Strike Rate)
-- ==============================================================================
-- Finding the top 10 run-scorers with their strike rates (Minimum 500 balls faced)
SELECT 
    batter AS player_name,
    SUM(batsman_runs) AS total_runs,
    COUNT(ball) AS balls_faced,
    ROUND((SUM(batsman_runs) * 100.0) / COUNT(ball), 2) AS strike_rate,
    SUM(CASE WHEN batsman_runs = 4 THEN 1 ELSE 0 END) AS total_fours,
    SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS total_sixes
FROM deliveries
GROUP BY batter
HAVING COUNT(ball) >= 500
ORDER BY total_runs DESC
LIMIT 10;

-- ==============================================================================
-- 2. Best Bowlers (Wickets & Economy Rate)
-- ==============================================================================
-- Finding top 10 bowlers based on wickets taken and economy rate (Min 50 overs bowled)
SELECT 
    bowler AS player_name,
    SUM(is_wicket) AS total_wickets,
    COUNT(ball) AS balls_bowled,
    COUNT(ball) / 6 AS overs_bowled,
    SUM(total_runs) AS runs_conceded,
    ROUND((SUM(total_runs) * 6.0) / COUNT(ball), 2) AS economy_rate
FROM deliveries
WHERE dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
GROUP BY bowler
HAVING (COUNT(ball) / 6) >= 50
ORDER BY total_wickets DESC, economy_rate ASC
LIMIT 10;

-- ==============================================================================
-- 3. Team Win Percentage by Season
-- ==============================================================================
WITH TeamMatches AS (
    SELECT season, team1 AS team FROM matches
    UNION ALL
    SELECT season, team2 AS team FROM matches
),
MatchesPlayed AS (
    SELECT season, team, COUNT(*) AS matches_played
    FROM TeamMatches
    GROUP BY season, team
),
MatchesWon AS (
    SELECT season, winner AS team, COUNT(*) AS matches_won
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY season, winner
)
SELECT 
    mp.season,
    mp.team,
    mp.matches_played,
    COALESCE(mw.matches_won, 0) AS matches_won,
    ROUND((COALESCE(mw.matches_won, 0) * 100.0) / mp.matches_played, 2) AS win_percentage
FROM MatchesPlayed mp
LEFT JOIN MatchesWon mw ON mp.season = mw.season AND mp.team = mw.team
ORDER BY mp.season DESC, win_percentage DESC;

-- ==============================================================================
-- 4. Toss Impact on Match Results
-- ==============================================================================
-- Does winning the toss increase the chance of winning the match?
SELECT 
    season,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_and_match_wins,
    ROUND((SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS toss_win_impact_percentage
FROM matches
WHERE winner IS NOT NULL
GROUP BY season
ORDER BY season DESC;

-- ==============================================================================
-- 5. Venue-Based Performance Analysis
-- ==============================================================================
-- Identifying high-scoring venues (Average runs per match)
WITH VenueScores AS (
    SELECT 
        m.venue,
        m.match_id,
        SUM(d.total_runs) AS match_total_runs
    FROM matches m
    JOIN deliveries d ON m.match_id = d.match_id
    GROUP BY m.venue, m.match_id
)
SELECT 
    venue,
    COUNT(match_id) AS matches_played,
    ROUND(AVG(match_total_runs), 2) AS avg_runs_per_match,
    MAX(match_total_runs) AS highest_match_aggregate
FROM VenueScores
GROUP BY venue
HAVING COUNT(match_id) >= 10
ORDER BY avg_runs_per_match DESC;

-- ==============================================================================
-- 6. Player Consistency Using Window Functions (RANK, DENSE_RANK)
-- ==============================================================================
-- Ranking batsmen per season based on total runs
WITH SeasonRuns AS (
    SELECT 
        m.season,
        d.batter AS player_name,
        SUM(d.batsman_runs) AS season_runs
    FROM matches m
    JOIN deliveries d ON m.match_id = d.match_id
    GROUP BY m.season, d.batter
)
SELECT 
    season,
    player_name,
    season_runs,
    RANK() OVER (PARTITION BY season ORDER BY season_runs DESC) AS run_rank,
    DENSE_RANK() OVER (PARTITION BY season ORDER BY season_runs DESC) AS run_dense_rank
FROM SeasonRuns
ORDER BY season DESC, run_rank ASC;

-- ==============================================================================
-- 7. Death Overs Performance (Last 5 Overs Analysis)
-- ==============================================================================
-- Finding the most destructive batsmen in death overs (overs 16-20)
-- Note: Overs are usually 0-indexed in some datasets or 1-indexed (we assume over >= 15 for 16-20)
SELECT 
    batter AS player_name,
    SUM(batsman_runs) AS runs_in_death,
    COUNT(ball) AS balls_faced,
    ROUND((SUM(batsman_runs) * 100.0) / COUNT(ball), 2) AS death_strike_rate,
    SUM(CASE WHEN batsman_runs = 4 THEN 1 ELSE 0 END) AS fours,
    SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS sixes
FROM deliveries
WHERE over >= 15  -- Assuming overs 0 to 19 format
GROUP BY batter
HAVING COUNT(ball) >= 100
ORDER BY death_strike_rate DESC
LIMIT 15;

-- ==============================================================================
-- 8. Most Economical Death Bowlers
-- ==============================================================================
SELECT 
    bowler AS player_name,
    COUNT(ball) / 6 AS overs_bowled_in_death,
    SUM(total_runs) AS runs_conceded,
    SUM(is_wicket) AS wickets_in_death,
    ROUND((SUM(total_runs) * 6.0) / COUNT(ball), 2) AS death_economy_rate
FROM deliveries
WHERE over >= 15
GROUP BY bowler
HAVING (COUNT(ball) / 6) >= 20
ORDER BY death_economy_rate ASC
LIMIT 10;
