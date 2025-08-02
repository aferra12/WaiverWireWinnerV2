WITH numbered_games AS (
  SELECT 
    gameDate,
    playerId,
    playerName,
    didPlay,
    isStarter,
    pitchesThrown,
    hilltopperPts,
    EXTRACT(YEAR FROM gameDate) as gameYear,
    ROW_NUMBER() OVER (PARTITION BY playerId, playerName, EXTRACT(YEAR FROM gameDate) ORDER BY gameDate) AS gameNumber
  FROM `sanguine-robot-454100-s3.waiver_wire_winner.player_game_logs`
  WHERE isPitcher
),

appearances_only AS (
  SELECT 
    gameDate,
    gameYear,
    playerId,
    playerName,
    pitchesThrown,
    hilltopperPts,
    gameNumber,
    LAG(gameNumber) OVER (PARTITION BY playerId, playerName, gameYear ORDER BY gameDate) AS prevAppGameNumber
  FROM numbered_games
  WHERE didPlay = TRUE AND isStarter = FALSE
),

games_rest AS (
SELECT 
  gameDate,
  gameYear,
  playerId,
  playerName,
  hilltopperPts,
  CASE 
    WHEN prevAppGameNumber IS NULL THEN NULL
    ELSE gameNumber - prevAppGameNumber - 1
  END AS gamesRest
FROM appearances_only
ORDER BY playerName, gameDate
),

max_game_number_pitched AS (
  SELECT
    playerId,
    playerName,
    MAX(gameNumber) AS maxGameNumPitched
  FROM appearances_only
  WHERE gameYear = EXTRACT(YEAR FROM CURRENT_DATE())
  GROUP BY playerId, playerName
),

max_game_number AS (
  SELECT
    playerId,
    playerName,
    -- Here is adding an extra day to rest if they had an off day (but likely still on roster)
    -- Will need an extra 26 man roster check on the backend though still
    IF(MAX(gameDate) = CURRENT_DATE() - 1, MAX(gameNumber), MAX(gameNumber) + 1) AS maxGameNum
  FROM numbered_games
  WHERE gameYear = EXTRACT(YEAR FROM CURRENT_DATE())
  GROUP BY playerId, playerName
),

pitches_last_thrown AS (
  SELECT
    ao.playerId,
    ao.playerName,
    pitchesThrown
  FROM appearances_only ao
  JOIN max_game_number_pitched mgnp
  ON ao.playerId = mgnp.playerId AND ao.prevAppGameNumber = mgnp.maxGameNumPitched
),

median_games_rest AS (
  SELECT 
    gr.playerId,
    gr.playerName,
    gameYear,
    CASE
      WHEN PERCENTILE_CONT(gamesRest, 0.6) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) >= 0 AND PERCENTILE_CONT(gamesRest, 0.6) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) < 1 AND plt.pitchesThrown > 60 THEN 4
      WHEN PERCENTILE_CONT(gamesRest, 0.6) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) >= 0 AND PERCENTILE_CONT(gamesRest, 0.6) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) < 1 AND plt.pitchesThrown < 60 THEN 2
      WHEN PERCENTILE_CONT(gamesRest, 0.6) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) >= 1 THEN PERCENTILE_CONT(gamesRest, 0.6) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear)
    END AS medianGamesRestWindow,
    -- AVG(daysRest) OVER(PARTITION BY playerName, gameYear) AS avg_days_rest_window,
    AVG(hilltopperPts) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) AS avgFantasyPts,
    PERCENTILE_CONT(hilltopperPts, 0.75) OVER(PARTITION BY gr.playerId, gr.playerName, gameYear) AS boomFantasyPoints,
  FROM games_rest gr
  JOIN pitches_last_thrown plt
  ON gr.playerId = plt.playerId
  WHERE gamesRest IS NOT NULL
),

median_games_rest_table AS (
  SELECT
    playerId,
    playerName,
    gameYear,
    max(medianGamesRestWindow) as medianGamesRest,
    max(avgFantasyPts) as avgFantasyPts,
    max(boomFantasyPoints) as boomFantasyPoints
    -- max(avg_days_rest_window)
  FROM median_games_rest
  GROUP BY playerId, playerName, gameYear
),

current_games_rest_table AS (
  SELECT
    mgn.playerId,
    mgn.playerName,
    maxGameNum - maxGameNumPitched AS gamesRest
  FROM max_game_number mgn
  JOIN max_game_number_pitched mgnp
  ON mgn.playerId = mgnp.playerId
  ORDER BY gamesRest desc
)

SELECT
  cgr.playerId,
  cgr.playerName,
  cgr.gamesRest,
  mgr.medianGamesRest,
  mgr.avgFantasyPts,
  mgr.boomFantasyPoints
FROM current_games_rest_table cgr
JOIN median_games_rest_table mgr
ON cgr.playerId = mgr.playerId
WHERE
  mgr.gameYear = EXTRACT(YEAR FROM CURRENT_DATE())
  AND cgr.gamesRest >= mgr.medianGamesRest
  AND cgr.gamesRest < 10
ORDER BY boomFantasyPoints DESC