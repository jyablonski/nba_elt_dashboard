CREATE SCHEMA nba_prod;
CREATE SCHEMA ml_models;
SET search_path TO nba_prod;

DROP TABLE IF EXISTS bans;
CREATE TABLE IF NOT EXISTS bans
(
    upcoming_games integer,
    upcoming_game_date date,
    location text COLLATE pg_catalog."default",
    tot_wins integer,
    games_played integer,
    avg_pts numeric,
    last_yr_ppg numeric,
    scrape_time timestamp without time zone,
    win_pct numeric,
    league_ts_percent numeric,
    last_updated_at timestamp without time zone,
    run_type text COLLATE pg_catalog."default",
    most_recent_game date,
    sum_active_protocols numeric,
    sum_active_protocols_lastwk numeric,
    protocols_differential numeric,
    protocols_pct_diff numeric,
    protocols_text text COLLATE pg_catalog."default"
);
INSERT INTO bans(
	upcoming_games, upcoming_game_date, location, tot_wins, games_played, avg_pts, last_yr_ppg, scrape_time, win_pct, league_ts_percent, last_updated_at, run_type, most_recent_game, sum_active_protocols, sum_active_protocols_lastwk, protocols_differential, protocols_pct_diff, protocols_text)
	VALUES (3, current_date, 'H', 714, 1230, 114.68, 112.1, current_timestamp, 0.580, 0.581, current_timestamp, 'dbt_docker', current_date, 0, 0, 0, 0, 'No Difference'),
           (3, current_date, 'A', 516, 1230, 114.68, 112.1, current_timestamp, 0.420, 0.581, current_timestamp, 'dbt_docker', current_date, 0, 0, 0, 0, 'No Difference');


-- boostrap script boiiiiiiiii
DROP TABLE IF EXISTS standings;
CREATE TABLE standings(
    rank text,
    team text,
    team_full text,
    conference text,
    wins bigint,
    losses bigint,
    games_played bigint,
    win_pct numeric,
    active_injuries numeric,
    active_protocols numeric,
    last_10 text
);

INSERT INTO standings (rank, team, team_full, conference, wins, losses, games_played, win_pct, active_injuries, active_protocols, last_10)
VALUES ('1st', 'MIL', 'Milwaukee Bucks', 'Eastern', 57, 22, 79, 0.722, 3, 1, '7-3'),
       ('2nd', 'BOS', 'Boston Celtics', 'Eastern', 25, 54, 79, 0.316, 4, 0, '2-8'),
       ('1st', 'MIL', 'Milwaukee Bucks', 'Western', 50, 29, 79, 0.633, 3, 2, '8-3'),
       ('2nd', 'BOS', 'Boston Celtics', 'Western', 48, 31, 79, 0.607, 4, 0, '4-6');
5
DROP TABLE IF EXISTS scorers;
CREATE TABLE scorers(
    player text,
    team text,
    full_team text,
    season_avg_ppg numeric,
    playoffs_avg_ppg numeric,
    season_ts_percent numeric,
    playoffs_ts_percent numeric,
    games_played bigint,
    playoffs_games_played bigint,
    ppg_rank bigint,
    top20_scorers text,
    player_mvp_calc_adj numeric,
    games_missed bigint,
    penalized_games_missed numeric,
    top5_candidates text,
    mvp_rank bigint
);

INSERT INTO scorers (player, team, full_team, season_avg_ppg, playoffs_avg_ppg, season_ts_percent, playoffs_ts_percent, games_played, playoffs_games_played,
                          ppg_rank, top20_scorers, player_mvp_calc_adj, games_missed, penalized_games_missed, top5_candidates, mvp_rank)
VALUES ('Nikola Jokic', 'DEN', 'Denver Nuggets', 24.8, null, 0.702, null, 68, null, 23, 'Other', 48.70, 11, 0, 'Top 5 MVP Candidate', 1),
       ('Shai Gilgeous-Alexander', 'OKC', 'Okalahoma City Thunder', 31.5, null, 0.628, null, 67, null, 4, 'Top 20 Scorers', 44.10, 13, 0,
        'Top 5 MVP Candidate', 5);

DROP TABLE IF EXISTS team_ratings;
CREATE TABLE team_ratings(
    team text,
    team_acronym text,
    w integer,
    l integer,
    ortg numeric,
    drtg numeric,
    nrtg numeric,
    team_logo text,
    nrtg_rank text,
    drtg_rank text,
    ortg_rank text
);

INSERT INTO team_ratings (team, team_acronym, w, l, ortg, drtg, nrtg, team_logo, nrtg_rank, drtg_rank, ortg_rank)
VALUES ('Boston Celtics', 'BOS', 54, 25, 118, 111.6, 6.4, 'logos/bos.png', '1st', '3rd', '2nd'),
       ('Cleveland Cavaliers', 'CLE', 50, 30, 116.4, 110.8, 5.6, 'logos/cle.png', '2nd', '1st', '8th');

DROP TABLE IF EXISTS twitter_comments;
CREATE TABLE twitter_comments(
    created_at date,
    scrape_ts timestamp without time zone,
    username text,
    tweet text,
    url text,
    likes numeric,
    retweets numeric,
    compound numeric,
    neg numeric,
    neu numeric,
    pos numeric
);

INSERT INTO twitter_comments (created_at, scrape_ts, username, tweet, url, likes, retweets, compound, neg, neu, pos)
VALUES (current_date, current_timestamp, 'KingJames', 'Man thats SIMPLY INSANE!!!! 🤣🤣🤣🤣🤣🤣🤣🤣🤣 https://t.co/WqyIWKHs4T',
        'https://twitter.com/twitter/statuses/1640515719896141826', 205431, 12757, 0, 0, 1, 0),
       (current_date, current_timestamp, 'FOS', 'The NCAA Womens National Championships 9.9 million viewers are more than',
        'https://twitter.com/twitter/statuses/1643051889846525953', 205431, 12757, 0, 0, 1, 0);

DROP TABLE IF EXISTS reddit_comments;
CREATE TABLE reddit_comments(
    scrape_date date,
    author text,
    comment text,
    flair text,
    score bigint,
    url text,
    compound numeric,
    pos numeric,
    neu numeric,
    neg numeric
);

INSERT INTO reddit_comments (scrape_date, author, comment, flair, score, url, compound, pos, neu, neg)
VALUES (current_date, 'rattatatouille', 'Jokic putting up a dismal effort', 'Spurs', 5875, 
        'https://www.reddit.com/r/nba/comments/12c4y8y/nikola_jokic_disasterclass_against_houston_14/',
        -0.6124, 0, 0.846, 0.154),
       (current_date, 'KaiserKaiba', 'NBA scriptwriters working overtime right now', null, 2829,
        'https://www.reddit.com/r/nba/comments/12c4y8y/nikola_jokic_disasterclass_against_houston_14/',
        0, 0, 1, 0);

DROP TABLE IF EXISTS injuries;
CREATE TABLE injuries(
    injury_pk text,
    player text,
    team_acronym text,
    team text,
    date text,
    status text,
    injury text,
    description text,
    total_injuries bigint,
    team_active_injuries numeric,
    team_active_protocols numeric,
    scrape_date date
);

INSERT INTO injuries (injury_pk, player, team_acronym, team, date, status, injury, description,
                           total_injuries, team_active_injuries, team_active_protocols, scrape_date)
VALUES ('09a97226ecd7b666dd516039ce752720', 'Myles Turner', 'IND', 'Indiana Pacers', 'Tues, Apr 4, 2023',
        'Day to Day', 'Ankle/Back', 'Turner is questionable for Wednesdays (Apr.5) game against New York.', 4, 4, 0, current_date),
       ('0e6fe518fdecea9c84ad54608810a528', 'Tyrese Haliburton', 'Haliburton is out for Wednesdays (Apr.5) game against New York.',
        'IND', 'Indiana Pacers', 'Tues, Apr 4, 2023', 'Out', 'Ankle', 4, 4, 0, current_date);


DROP TABLE IF EXISTS game_types;
CREATE TABLE IF NOT EXISTS injury_tracker
(
    player_logo text COLLATE pg_catalog."default",
    player text COLLATE pg_catalog."default",
    status text COLLATE pg_catalog."default",
    continuous_games_missed bigint,
    games_played bigint,
    season_avg_ppg numeric,
    player_mvp_calc_avg numeric,
    season_ts_percent numeric,
    season_avg_plusminus numeric
);

INSERT INTO injury_tracker(
	player_logo, player, status, continuous_games_missed, games_played, season_avg_ppg, player_mvp_calc_avg, season_ts_percent, season_avg_plusminus)
	VALUES ('https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629630.png', "<span style='font-size:16px; color:royalblue;'>Ja Morant</span> <span style='font-size:12px; color:grey;'>MEM</span>", 'Out - Suspension', 0, 61, 26.2, 41.4, 0.557, 5.0),
           ('https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629645.png', "<span style='font-size:16px; color:royalblue;'>Kevin Porter</span> <span style='font-size:12px; color:grey;'>HOU</span>", 'Day To Day - Possible suspension', 1, 59, 19.2, 26.1, 0.565, -5.8);

DROP TABLE IF EXISTS game_types;
CREATE TABLE game_types(
    game_type text,
    type text,
    n bigint,
    explanation text
);

INSERT INTO game_types (game_type, type, n, explanation)
VALUES ('20 pt Game', 'Regular Season', 356, 'between 11 and 20 points'),
       ('Blowout Game', 'Regular Season', 154, 'more than 20 points'),
       ('10 pt Game', 'Regular Season', 351, 'between 6 and 10 points'),
       ('Clutch Game', 'Regular Season', 327, '5 points or less');

DROP TABLE IF EXISTS feedback;
CREATE TABLE feedback(
    id serial primary key,
    feedback character varying,
    time timestamp without time zone
);

DROP TABLE IF EXISTS schedule;
CREATE TABLE schedule(
    date date,
    day text,
    avg_team_rank bigint,
    start_time text,
    home_team text,
    away_team text,
    home_moneyline_raw numeric,
    away_moneyline_raw numeric
);

INSERT INTO schedule (date, day, avg_team_rank, start_time, home_team, away_team, home_moneyline_raw, away_moneyline_raw)
VALUES (current_date, 'Monday', 16, '7:00 PM', 'Indiana Pacers', 'New York Knicks', 300, -365),
       (current_date, 'Monday', 20, '7:00 PM', 'New York Knicks', 'Indiana Pacers', -365, 300);

DROP TABLE IF EXISTS nba_predictions;
CREATE TABLE nba_predictions(
    proper_date date,
    home_team text,
    home_team_odds double precision,
    home_team_predicted_win_pct numeric,
    away_team text,
    away_team_odds double precision,
    away_team_predicted_win_pct numeric
);

INSERT INTO nba_predictions (proper_date, home_team, home_team_odds, home_team_predicted_win_pct, away_team, away_team_odds, away_team_predicted_win_pct)
VALUES (date(current_timestamp - interval '5 hour'), 'Indiana Pacers', '+200', 0.247, 'San Antonio Spurs', '-160', 0.753),
       (date(current_timestamp - interval '5 hour'), 'Houston Rockets', '-140', 0.194, 'Memphis Grizzlies', '+180', 0.806),
       (date(current_timestamp - interval '5 hour'), 'Golden State Warriors', '-150', 0.712, 'Boston Celtics', '180', 0.288),
       (date(current_timestamp - interval '5 hour'), 'Dallas Mavericks', '-140', 0.194, 'Detroit Pistons', '+180', 0.806),
       (date(current_timestamp - interval '5 hour'), 'Chicago Bulls', '+200', 0.355, 'Charlotte Hornets', '-160', 0.645),
       (date(current_timestamp - interval '5 hour'), 'Utah Jazz', '+320', 0.194, 'Phoenix Suns', '-250', 0.806);


DROP TABLE IF EXISTS transactions;
CREATE TABLE IF NOT EXISTS transactions
(
    date date,
    transaction text COLLATE pg_catalog."default"
);

INSERT INTO transactions(date, transaction)
VALUES (current_date, 'The Portland Trail Blazers signed Skylar Mays.'),
       (current_date, 'The Toronto Raptors fired Nick Nurse as Head Coach.');



-- 2023-05-28 update: this table is made from dbt in prod.  for testing im just making a blank table to test 
-- past bets functionality.
DROP TABLE IF EXISTS mov;
CREATE TABLE IF NOT EXISTS mov
(
    team text COLLATE pg_catalog."default",
    full_team text COLLATE pg_catalog."default",
    game_id bigint,
    date date,
    outcome text COLLATE pg_catalog."default",
    opponent text COLLATE pg_catalog."default",
    pts_scored numeric,
    pts_scored_opp numeric,
    mov numeric,
    record text COLLATE pg_catalog."default"
);

DROP TABLE IF EXISTS feature_flags;
CREATE TABLE IF NOT EXISTS feature_flags
(
	id serial primary key,
	flag text,
	is_enabled integer,
	created_at timestamp without time zone default now(),
	modified_at timestamp without time zone default now(),
    CONSTRAINT flag_unique UNIQUE (flag)
);
INSERT INTO feature_flags(flag, is_enabled)
VALUES ('season', 1),
       ('playoffs', 1);
