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

DROP TABLE IF EXISTS contract_value_analysis;
CREATE TABLE IF NOT EXISTS contract_value_analysis (
	player text NULL,
	salary_rank text NULL,
	team text NULL,
	games_played int8 NULL,
	player_mvp_calc_avg numeric NULL,
	salary numeric NULL,
	team_games_played int8 NULL,
	games_missed int8 NULL,
	pvm_rank numeric NULL,
	rankingish numeric NULL,
	percentile_rank numeric NULL,
	color_var text NULL,
	adj_penalty_final numeric NULL,
	pct_penalized numeric NULL
);

INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Nikola Jokic','$30+ M','DEN',69,48.30,47607350,82,13,32.77,1.000,100.000,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Luka Doncic','$30+ M','DAL',66,48.10,40064220,82,16,32.77,0.977,97.700,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Joel Embiid','$30+ M','PHI',66,47.80,47607350,82,16,32.77,0.953,95.300,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Shai Gilgeous-Alexander','$30+ M','OKC',68,44.00,33386850,82,14,32.77,0.930,93.000,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Jayson Tatum','$30+ M','BOS',74,43.80,32600060,82,8,32.77,0.907,90.700,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Giannis Antetokounmpo','$30+ M','MIL',63,42.86,45640084,82,19,32.77,0.884,88.400,'Superstars',0.94000000000000000000,0.06000000000000000000),
	 ('Trae Young','$30+ M','ATL',73,39.90,40064220,82,9,32.77,0.860,86.000,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Donovan Mitchell','$30+ M','CLE',68,39.20,33162030,82,14,32.77,0.837,83.700,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Ja Morant','$30+ M','MEM',61,37.26,34005250,82,21,32.77,0.814,81.400,'Superstars',0.90000000000000000000,0.10000000000000000000),
	 ('Pascal Siakam','$30+ M','TOR',71,37.10,37893408,82,11,32.77,0.791,79.100,'Superstars',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Damian Lillard','$30+ M','POR',58,36.88,45640084,82,24,32.77,0.767,76.700,'Superstars',0.84000000000000000000,0.16000000000000000000),
	 ('De''Aaron Fox','$30+ M','SAC',73,36.60,32600060,82,9,32.77,0.744,74.400,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Darius Garland','$30+ M','CLE',69,36.30,34005250,82,13,32.77,0.721,72.100,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Jaylen Brown','$30+ M','BOS',67,35.80,31830357,82,15,32.77,0.698,69.800,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Domantas Sabonis','$30+ M','SAC',79,35.60,30600000,82,3,32.77,0.674,67.400,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Kyrie Irving','$30+ M','DAL',60,35.38,37037037,82,22,32.77,0.651,65.100,'Superstars',0.88000000000000000000,0.12000000000000000000),
	 ('Jalen Brunson','$25-30 M','NYK',68,35.30,26346666,82,14,26.37,1.000,100.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('DeMar DeRozan','$25-30 M','CHI',74,35.10,28600000,82,8,26.37,0.917,91.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Fred VanVleet','$30+ M','TOR',69,35.10,40806300,82,13,32.77,0.605,60.500,'Superstars',1.00000000000000000000,0.00000000000000000000),
	 ('Jrue Holiday','$30+ M','MIL',67,35.10,36861707,82,15,32.77,0.605,60.500,'Superstars',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Julius Randle','$25-30 M','NYK',77,35.00,28226880,82,5,26.37,0.833,83.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jimmy Butler','$30+ M','MIA',64,34.66,45183960,82,18,32.77,0.581,58.100,'Superstars',0.96000000000000000000,0.04000000000000000000),
	 ('Anthony Edwards','$10-15 M','MIN',79,34.60,13534817,82,3,15.50,1.000,100.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('James Harden','$30+ M','PHI',58,34.27,35640000,82,24,32.77,0.558,55.800,'Superstars',0.84000000000000000000,0.16000000000000000000),
	 ('LeBron James','$30+ M','LAL',55,33.77,47607350,82,27,32.77,0.535,53.500,'Superstars',0.78000000000000000000,0.22000000000000000000),
	 ('Stephen Curry','$30+ M','GSW',56,33.68,51915615,82,26,32.77,0.512,51.200,'Superstars',0.80000000000000000000,0.20000000000000000000),
	 ('Lauri Markkanen','$15-20 M','UTA',66,33.50,17259999,82,16,19.25,1.000,100.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Kristaps Porzingis','$30+ M','WAS',65,33.03,36016200,82,17,32.77,0.488,48.800,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('Anthony Davis','$30+ M','LAL',56,32.64,40600080,82,26,32.77,0.465,46.500,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Dejounte Murray','$15-20 M','ATL',74,32.10,18214000,82,8,19.25,0.966,96.600,'Great Value',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Jamal Murray','$30+ M','DEN',65,32.05,33833400,82,17,32.77,0.442,44.200,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('Zach LaVine','$30+ M','CHI',77,32.00,40064220,82,5,32.77,0.419,41.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Kevin Durant','$30+ M','PHX',47,31.50,47649433,82,35,32.77,0.395,39.500,'Normal',0.75,0.25),
	 ('CJ McCollum','$30+ M','NOP',75,31.30,35802469,82,7,32.77,0.372,37.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Bam Adebayo','$30+ M','MIA',75,30.80,32600060,82,7,32.77,0.349,34.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Tyrese Haliburton','$5-10 M','IND',56,30.64,5808435,82,26,13.69,1.000,100.000,'Great Value',0.80000000000000000000,0.20000000000000000000),
	 ('Jaren Jackson','$25-30 M','MEM',63,30.08,27102202,82,19,26.37,0.750,75.000,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Devin Booker','$30+ M','PHX',53,29.25,36016200,82,29,32.77,0.326,32.600,'Normal',0.75,0.25),
	 ('Mikal Bridges','$20-25 M','BKN',83,28.90,21700000,82,-1,23.68,1.000,100.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Aaron Gordon','$20-25 M','DEN',68,28.80,22266182,82,14,23.68,0.944,94.400,'Great Value',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Evan Mobley','$5-10 M','CLE',79,28.80,8882640,82,3,13.69,0.987,98.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Tyler Herro','$25-30 M','MIA',67,28.80,27000000,82,15,26.37,0.667,66.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Klay Thompson','$30+ M','GSW',69,28.30,43219440,82,13,32.77,0.302,30.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Spencer Dinwiddie','$20-25 M','BKN',79,28.30,20357143,82,3,23.68,0.889,88.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Nikola Vucevic','$15-20 M','CHI',82,28.20,18518519,82,0,19.25,0.931,93.100,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('D''Angelo Russell','$15-20 M','LAL',71,28.00,17307693,82,11,19.25,0.897,89.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Paul George','$30+ M','LAC',56,27.92,45640084,82,26,32.77,0.279,27.900,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Zion Williamson','$30+ M','NOP',29,27.83,34005250,82,53,32.77,0.256,25.600,'Normal',0.75,0.25),
	 ('Russell Westbrook','< $5 M','LAC',73,27.70,3835738,82,9,7.19,1.000,100.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Scottie Barnes','$5-10 M','TOR',77,27.70,8008680,82,5,13.69,0.975,97.500,'Great Value',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Desmond Bane','< $5 M','MEM',58,27.64,3845083,82,24,7.19,0.997,99.700,'Great Value',0.84000000000000000000,0.16000000000000000000),
	 ('Brook Lopez','$25-30 M','MIL',78,27.50,25000000,82,4,26.37,0.583,58.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Kawhi Leonard','$30+ M','LAC',52,27.23,45640084,82,30,32.77,0.233,23.300,'Normal',0.75,0.25),
	 ('Josh Giddey','$5-10 M','OKC',76,27.20,6587040,82,6,13.69,0.962,96.200,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Kyle Kuzma','$25-30 M','WAS',64,26.98,25568182,82,18,26.37,0.500,50.000,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Chris Paul','$30+ M','PHX',59,26.57,30800000,82,23,32.77,0.209,20.900,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('Terry Rozier','$20-25 M','CHA',63,26.51,23205221,82,19,23.68,0.833,83.300,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Jarrett Allen','$20-25 M','CLE',68,26.20,20000000,82,14,23.68,0.778,77.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('LaMelo Ball','$10-15 M','CHA',36,26.10,10900635,82,46,15.50,0.956,95.600,'Great Value',0.75,0.25),
	 ('Paolo Banchero','$10-15 M','ORL',72,26.10,11608080,82,10,15.50,0.956,95.600,'Great Value',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Brandon Ingram','$30+ M','NOP',45,25.95,33833400,82,37,32.77,0.186,18.600,'Bad Value',0.75,0.25),
	 ('Jordan Poole','$25-30 M','GSW',82,25.90,27455357,82,0,26.37,0.417,41.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Nic Claxton','$5-10 M','BKN',76,25.70,9625000,82,6,13.69,0.949,94.900,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('OG Anunoby','$15-20 M','TOR',67,25.60,18642857,82,15,19.25,0.862,86.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Tyrese Maxey','< $5 M','PHI',60,25.52,4343920,82,22,7.19,0.993,99.300,'Great Value',0.88000000000000000000,0.12000000000000000000),
	 ('Franz Wagner','$5-10 M','ORL',80,25.40,5508720,82,2,13.69,0.937,93.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Deandre Ayton','$30+ M','PHX',67,25.30,32459438,82,15,32.77,0.163,16.300,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Jerami Grant','$25-30 M','POR',63,25.00,27586207,82,19,26.37,0.333,33.300,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Jalen Green','$5-10 M','HOU',76,24.70,9891480,82,6,13.69,0.924,92.400,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Myles Turner','$20-25 M','IND',63,24.63,20975000,82,19,23.68,0.722,72.200,'Normal',0.94000000000000000000,0.06000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Immanuel Quickley','< $5 M','NYK',81,24.60,4171548,82,1,7.19,0.990,99.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Anfernee Simons','$20-25 M','POR',62,24.47,24107143,82,20,23.68,0.667,66.700,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Derrick White','$15-20 M','BOS',82,24.40,18357143,82,0,19.25,0.828,82.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Bradley Beal','$30+ M','WAS',50,24.38,46741590,82,32,32.77,0.140,14.000,'Bad Value',0.75,0.25),
	 ('Draymond Green','$20-25 M','GSW',73,24.20,22321429,82,9,23.68,0.611,61.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Tobias Harris','$30+ M','PHI',75,24.10,39270150,82,7,32.77,0.116,11.600,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Jordan Clarkson','$20-25 M','UTA',61,24.03,23487629,82,21,23.68,0.556,55.600,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Mike Conley','$20-25 M','MIN',67,24.00,24360000,82,15,23.68,0.500,50.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('RJ Barrett','$20-25 M','NYK',73,23.70,23883929,82,9,23.68,0.444,44.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Malcolm Brogdon','$20-25 M','BOS',67,23.60,22500000,82,15,23.68,0.389,38.900,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Michael Porter','$30+ M','DEN',62,23.55,33386850,82,20,32.77,0.093,9.300,'Bad Value',0.92000000000000000000,0.08000000000000000000),
	 ('Kevin Huerter','$15-20 M','SAC',75,23.50,15669643,82,7,19.25,0.793,79.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Buddy Hield','$15-20 M','IND',80,23.30,19279841,82,2,19.25,0.759,75.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Karl-Anthony Towns','$30+ M','MIN',29,23.18,36016200,82,53,32.77,0.070,7.000,'Bad Value',0.75,0.25),
	 ('Alperen Sengun','< $5 M','HOU',75,23.10,3536280,82,7,7.19,0.987,98.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Christian Wood','< $5 M','DAL',67,23.00,1000000,82,15,7.19,0.984,98.400,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Gary Trent','$15-20 M','TOR',66,23.00,18560000,82,16,19.25,0.724,72.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Rudy Gobert','$30+ M','MIN',70,22.70,41000000,82,12,32.77,0.047,4.700,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Tre Jones','$5-10 M','SAS',68,22.60,9895833,82,14,13.69,0.911,91.100,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Kevin Porter','$15-20 M','HOU',59,22.45,15860000,82,23,19.25,0.690,69.000,'Normal',0.86000000000000000000,0.14000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Marcus Smart','$15-20 M','BOS',61,22.23,18833713,82,21,19.25,0.655,65.500,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Jalen Williams','< $5 M','OKC',75,22.20,4558680,82,7,7.19,0.980,98.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Keldon Johnson','$20-25 M','SAS',63,22.18,20000000,82,19,23.68,0.333,33.300,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Josh Hart','$10-15 M','NYK',76,22.00,12960000,82,6,15.50,0.933,93.300,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Kyle Anderson','$5-10 M','MIN',69,21.90,9219512,82,13,13.69,0.899,89.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jakob Poeltl','$15-20 M','TOR',72,21.80,19500000,82,10,19.25,0.621,62.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Dillon Brooks','$20-25 M','MEM',73,21.40,22627671,82,9,23.68,0.278,27.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Caris LeVert','$15-20 M','CLE',74,21.30,15384616,82,8,19.25,0.586,58.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Kentavious Caldwell-Pope','$10-15 M','DEN',76,21.20,14704938,82,6,15.50,0.911,91.100,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Harrison Barnes','$15-20 M','SAC',82,21.10,17000000,82,0,19.25,0.552,55.200,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('P.J. Washington','< $5 M','CHA',73,20.90,1000000,82,9,7.19,0.977,97.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Bobby Portis','$10-15 M','MIL',70,20.80,11710818,82,12,15.50,0.867,86.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Dennis Schroder','$10-15 M','LAL',66,20.80,12405000,82,16,15.50,0.867,86.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Trey Murphy','< $5 M','NOP',79,20.80,3359280,82,3,7.19,0.974,97.400,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Clint Capela','$20-25 M','ATL',65,20.78,20616000,82,17,23.68,0.222,22.200,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('Markelle Fultz','$15-20 M','ORL',60,20.77,17000000,82,22,19.25,0.517,51.700,'Normal',0.88000000000000000000,0.12000000000000000000),
	 ('Tyus Jones','$10-15 M','MEM',80,20.70,14000000,82,2,15.50,0.844,84.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Cade Cunningham','$10-15 M','DET',12,20.63,11055360,82,70,15.50,0.822,82.200,'Normal',0.75,0.25),
	 ('Jonas Valanciunas','$15-20 M','NOP',79,20.60,15435000,82,3,19.25,0.483,48.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Al Horford','$10-15 M','BOS',63,20.49,10000000,82,19,15.50,0.800,80.000,'Normal',0.94000000000000000000,0.06000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Kelly Olynyk','$10-15 M','UTA',68,20.40,12195122,82,14,15.50,0.778,77.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Tim Hardaway','$15-20 M','DAL',71,20.40,17897728,82,11,19.25,0.448,44.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Luguentz Dort','$15-20 M','OKC',74,20.10,15277778,82,8,19.25,0.414,41.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Andrew Wiggins','$20-25 M','GSW',37,20.03,24330357,82,45,23.68,0.167,16.700,'Bad Value',0.75,0.25),
	 ('Bruce Brown','$20-25 M','DEN',80,20.00,22000000,82,2,23.68,0.111,11.100,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Malik Monk','$5-10 M','SAC',77,20.00,9945830,82,5,13.69,0.886,88.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('John Collins','$25-30 M','ATL',71,19.60,25340000,82,11,26.37,0.250,25.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Austin Reaves','$10-15 M','LAL',64,19.58,12015150,82,18,15.50,0.756,75.600,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Walker Kessler','< $5 M','UTA',74,19.40,2831160,82,8,7.19,0.970,97.000,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Bojan Bogdanovic','$20-25 M','DET',59,19.35,20000000,82,23,23.68,0.056,5.600,'Bad Value',0.86000000000000000000,0.14000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Herbert Jones','$10-15 M','NOP',66,19.10,12015150,82,16,15.50,0.733,73.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jaden Ivey','$5-10 M','DET',74,19.10,7614480,82,8,13.69,0.873,87.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('De''Anthony Melton','$5-10 M','PHI',77,19.00,8000000,82,5,13.69,0.861,86.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('De''Andre Hunter','$20-25 M','ATL',68,18.90,20089286,82,14,23.68,0.000,0.000,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Jaden McDaniels','< $5 M','MIN',79,18.90,3901399,82,3,7.19,0.967,96.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Khris Middleton','$25-30 M','MIL',33,18.83,29320988,82,49,26.37,0.167,16.700,'Bad Value',0.75,0.25),
	 ('Louis King','< $5 M','PHI',1,18.75,1000000,82,81,7.19,0.964,96.400,'Great Value',0.75,0.25),
	 ('Monte Morris','$5-10 M','WAS',62,18.58,9800926,82,20,13.69,0.848,84.800,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Bennedict Mathurin','$5-10 M','IND',78,18.50,6916080,82,4,13.69,0.823,82.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Mason Plumlee','$5-10 M','LAC',79,18.50,5000000,82,3,13.69,0.823,82.300,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Donte DiVincenzo','$10-15 M','GSW',72,18.40,10900000,82,10,15.50,0.711,71.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Cole Anthony','$5-10 M','ORL',60,18.39,5539771,82,22,13.69,0.810,81.000,'Normal',0.88000000000000000000,0.12000000000000000000),
	 ('Skylar Mays','< $5 M','POR',6,18.38,1000000,82,76,7.19,0.961,96.100,'Great Value',0.75,0.25),
	 ('Keegan Murray','$5-10 M','SAC',80,18.30,8409000,82,2,13.69,0.797,79.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Saddiq Bey','< $5 M','ATL',77,18.30,4556983,82,5,7.19,0.957,95.700,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Royce O''Neale','$5-10 M','BKN',76,18.20,9500000,82,6,13.69,0.785,78.500,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Shaquille Harrison','< $5 M','LAL',5,18.15,1000000,82,77,7.19,0.954,95.400,'Great Value',0.75,0.25),
	 ('Wendell Carter','$10-15 M','ORL',57,18.12,13050000,82,25,15.50,0.689,68.900,'Normal',0.82000000000000000000,0.18000000000000000000),
	 ('Ivica Zubac','$10-15 M','LAC',76,18.10,10933333,82,6,15.50,0.667,66.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Kevon Looney','$5-10 M','GSW',82,18.10,7500000,82,0,13.69,0.772,77.200,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Cameron Johnson','$25-30 M','BKN',42,18.00,25679348,82,40,26.37,0.083,8.300,'Bad Value',0.75,0.25),
	 ('Mac McClung','< $5 M','PHI',2,18.00,1000000,82,80,7.19,0.951,95.100,'Great Value',0.75,0.25),
	 ('Onyeka Okongwu','$5-10 M','ATL',80,18.00,8109063,82,2,13.69,0.759,75.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Killian Hayes','$5-10 M','DET',76,17.90,7413955,82,6,13.69,0.747,74.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Quentin Grimes','< $5 M','NYK',71,17.90,2385720,82,11,7.19,0.948,94.800,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Norman Powell','$15-20 M','LAC',60,17.78,18000000,82,22,19.25,0.379,37.900,'Normal',0.88000000000000000000,0.12000000000000000000),
	 ('Grayson Allen','$5-10 M','MIL',72,17.60,8925000,82,10,13.69,0.734,73.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Kris Dunn','< $5 M','UTA',22,17.48,2586665,82,60,7.19,0.944,94.400,'Great Value',0.75,0.25),
	 ('Kelly Oubre','< $5 M','CHA',48,17.40,1000000,82,34,7.19,0.941,94.100,'Great Value',0.75,0.25),
	 ('T.J. McConnell','$5-10 M','IND',75,17.20,8700000,82,7,13.69,0.722,72.200,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Devin Vassell','$5-10 M','SAS',38,17.10,5887899,82,44,13.69,0.709,70.900,'Normal',0.75,0.25),
	 ('Mitchell Robinson','$15-20 M','NYK',60,16.98,15681818,82,22,19.25,0.345,34.500,'Normal',0.88000000000000000000,0.12000000000000000000),
	 ('Talen Horton-Tucker','$10-15 M','UTA',65,16.86,11020000,82,17,15.50,0.644,64.400,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('Kyle Lowry','$25-30 M','MIA',55,16.69,29682540,82,27,26.37,0.000,0.000,'Bad Value',0.78000000000000000000,0.22000000000000000000),
	 ('Jusuf Nurkic','$15-20 M','POR',52,16.58,16875000,82,30,19.25,0.310,31.000,'Normal',0.75,0.25),
	 ('Steven Adams','$10-15 M','MEM',42,16.35,12600000,82,40,15.50,0.622,62.200,'Normal',0.75,0.25),
	 ('Coby White','$10-15 M','CHI',74,16.30,11111111,82,8,15.50,0.600,60.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Deni Avdija','$5-10 M','WAS',76,16.30,6263188,82,6,13.69,0.696,69.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Malik Beasley','< $5 M','LAL',81,16.30,2019706,82,1,7.19,0.938,93.800,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Marcus Morris','$15-20 M','LAC',65,15.97,17116279,82,17,19.25,0.276,27.600,'Normal',0.98000000000000000000,0.02000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Zach Collins','$5-10 M','SAS',63,15.89,7700000,82,19,13.69,0.684,68.400,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Gordon Hayward','$30+ M','CHA',50,15.83,31500000,82,32,32.77,0.023,2.300,'Bad Value',0.75,0.25),
	 ('Jabari Smith','$5-10 M','HOU',79,15.80,9326520,82,3,13.69,0.671,67.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Bogdan Bogdanovic','$15-20 M','ATL',54,15.73,18700000,82,28,19.25,0.241,24.100,'Normal',0.76000000000000000000,0.24000000000000000000),
	 ('Caleb Martin','$5-10 M','MIA',71,15.70,6802950,82,11,13.69,0.658,65.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Andrew Nembhard','< $5 M','IND',75,15.50,2131905,82,7,7.19,0.928,92.800,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Eric Gordon','< $5 M','LAC',69,15.50,3196448,82,13,7.19,0.928,92.800,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Kenyon Martin','< $5 M','HOU',82,15.50,1930681,82,0,7.19,0.928,92.800,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Max Strus','$10-15 M','MIA',80,15.50,14487684,82,2,15.50,0.556,55.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Naz Reid','$10-15 M','MIN',68,15.50,12950400,82,14,15.50,0.556,55.600,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Alex Caruso','$5-10 M','CHI',67,15.40,9460000,82,15,13.69,0.646,64.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jarred Vanderbilt','< $5 M','LAL',78,15.40,4698000,82,4,7.19,0.925,92.500,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Santi Aldama','< $5 M','MEM',77,15.20,2194200,82,5,7.19,0.921,92.100,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Larry Nance','$10-15 M','NOP',65,15.19,10375000,82,17,15.50,0.533,53.300,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('RaiQuan Gray','< $5 M','BKN',1,15.00,1000000,82,81,7.19,0.918,91.800,'Great Value',0.75,0.25),
	 ('Ben Simmons','$30+ M','BKN',42,14.93,37893408,82,40,32.77,0.000,0.000,'Bad Value',0.75,0.25),
	 ('Reggie Jackson','$5-10 M','DEN',68,14.80,5000000,82,14,13.69,0.633,63.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Chris Boucher','$10-15 M','TOR',76,14.70,11750000,82,6,15.50,0.511,51.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Isaiah Joe','< $5 M','OKC',73,14.70,1997238,82,9,7.19,0.911,91.100,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Jaylen Nowell','< $5 M','MIN',65,14.70,1000000,82,17,7.19,0.911,91.100,'Great Value',0.98000000000000000000,0.02000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Patrick Williams','$5-10 M','CHI',82,14.70,9835881,82,0,13.69,0.620,62.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Daniel Gafford','$10-15 M','WAS',78,14.60,12402000,82,4,15.50,0.489,48.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Josh Richardson','< $5 M','NOP',65,14.60,2891467,82,17,7.19,0.905,90.500,'Great Value',0.98000000000000000000,0.02000000000000000000),
	 ('Tari Eason','< $5 M','HOU',82,14.60,3527160,82,0,7.19,0.905,90.500,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Grant Williams','$10-15 M','BOS',79,14.50,12405000,82,3,15.50,0.467,46.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Naji Marshall','< $5 M','NOP',77,14.50,1930681,82,5,7.19,0.902,90.200,'Great Value',1.00000000000000000000,0.00000000000000000000),
	 ('Jose Alvarado','< $5 M','NOP',61,14.49,1836096,82,21,7.19,0.898,89.800,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Robert Williams','$10-15 M','BOS',35,14.48,11571429,82,47,15.50,0.444,44.400,'Normal',0.75,0.25),
	 ('Dorian Finney-Smith','$10-15 M','BKN',66,14.30,13932008,82,16,15.50,0.422,42.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Shake Milton','$5-10 M','PHI',76,14.30,5000000,82,6,13.69,0.608,60.800,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Jalen Duren','< $5 M','DET',67,14.20,4330680,82,15,7.19,0.892,89.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jalen McDaniels','< $5 M','PHI',80,14.20,4516000,82,2,7.19,0.892,89.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jevon Carter','$5-10 M','MIL',81,14.20,6190476,82,1,13.69,0.595,59.500,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jonathan Kuminga','$5-10 M','GSW',67,14.10,6012840,82,15,13.69,0.582,58.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Terance Mann','$10-15 M','LAC',81,14.10,10576923,82,1,15.50,0.400,40.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Delon Wright','$5-10 M','WAS',50,14.03,8195122,82,32,13.69,0.570,57.000,'Normal',0.75,0.25),
	 ('Dennis Smith','< $5 M','CHA',54,13.98,2019706,82,28,7.19,0.889,88.900,'Normal',0.76000000000000000000,0.24000000000000000000),
	 ('Gabe Vincent','$10-15 M','MIA',68,13.90,10500000,82,14,15.50,0.378,37.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Rui Hachimura','$15-20 M','LAL',63,13.82,15740741,82,19,19.25,0.207,20.700,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Jalen Smith','$5-10 M','IND',68,13.80,5043773,82,14,13.69,0.557,55.700,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Ayo Dosunmu','$5-10 M','CHI',80,13.70,6481482,82,2,13.69,0.532,53.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Cedi Osman','$5-10 M','CLE',77,13.70,6718842,82,5,13.69,0.532,53.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Cameron Payne','$5-10 M','PHX',48,13.58,6500000,82,34,13.69,0.519,51.900,'Normal',0.75,0.25),
	 ('Collin Sexton','$15-20 M','UTA',48,13.58,17325000,82,34,19.25,0.172,17.200,'Bad Value',0.75,0.25),
	 ('Aaron Nesmith','$5-10 M','IND',73,13.50,5634257,82,9,13.69,0.506,50.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Patrick Beverley','< $5 M','CHI',67,13.50,2019706,82,15,7.19,0.885,88.500,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Corey Kispert','< $5 M','WAS',74,13.40,3722040,82,8,7.19,0.882,88.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('John Wall','$5-10 M','LAC',34,13.35,6802950,82,48,13.69,0.494,49.400,'Normal',0.75,0.25),
	 ('Bol Bol','< $5 M','ORL',70,13.30,2019706,82,12,7.19,0.879,87.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Alec Burks','$10-15 M','DET',51,13.28,10489600,82,31,15.50,0.356,35.600,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Kevin Love','< $5 M','MIA',62,13.25,3835738,82,20,7.19,0.875,87.500,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Josh Okogie','< $5 M','PHX',72,13.20,2815937,82,10,7.19,0.872,87.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Bones Hyland','< $5 M','LAC',56,13.04,2306400,82,26,7.19,0.869,86.900,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Drew Eubanks','< $5 M','POR',78,13.00,2346614,82,4,7.19,0.866,86.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Nicolas Batum','$10-15 M','LAC',78,13.00,11710818,82,4,15.50,0.333,33.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Victor Oladipo','$5-10 M','MIA',42,12.90,9450000,82,40,13.69,0.481,48.100,'Normal',0.75,0.25),
	 ('John Konchar','< $5 M','MEM',72,12.80,2400000,82,10,7.19,0.862,86.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Gabe York','< $5 M','IND',3,12.60,1000000,82,79,7.19,0.856,85.600,'Normal',0.75,0.25),
	 ('Isaiah Hartenstein','$5-10 M','NYK',82,12.60,9245121,82,0,13.69,0.468,46.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Torrey Craig','< $5 M','PHX',79,12.60,2528233,82,3,7.19,0.856,85.600,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Luke Kennard','$10-15 M','MEM',59,12.56,14763636,82,23,15.50,0.311,31.100,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('AJ Griffin','< $5 M','ATL',72,12.50,3712920,82,10,7.19,0.849,84.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Keita Bates-Diop','< $5 M','SAS',67,12.50,2346614,82,15,7.19,0.849,84.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Brandon Clarke','$10-15 M','MEM',56,12.48,12500000,82,26,15.50,0.289,28.900,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Pat Connaughton','$5-10 M','MIL',61,12.42,9423869,82,21,13.69,0.456,45.600,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Nick Richards','$5-10 M','CHA',65,12.35,5000000,82,17,13.69,0.443,44.300,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('Jalen Suggs','$5-10 M','ORL',53,12.15,7252080,82,29,13.69,0.430,43.000,'Normal',0.75,0.25),
	 ('Xavier Tillman','< $5 M','MEM',61,12.15,1930681,82,21,7.19,0.846,84.600,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Moritz Wagner','$5-10 M','ORL',57,12.14,8000000,82,25,13.69,0.418,41.800,'Normal',0.82000000000000000000,0.18000000000000000000),
	 ('Tre Mann','< $5 M','OKC',67,12.10,3191400,82,15,7.19,0.843,84.300,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Jeremy Sochan','$5-10 M','SAS',56,12.08,5316960,82,26,13.69,0.405,40.500,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Josh Green','< $5 M','DAL',60,11.97,4765339,82,22,7.19,0.839,83.900,'Normal',0.88000000000000000000,0.12000000000000000000),
	 ('Trey Lyles','$5-10 M','SAC',74,11.90,8000000,82,8,13.69,0.392,39.200,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Troy Brown','< $5 M','LAL',76,11.90,4000000,82,6,7.19,0.836,83.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Dwight Powell','< $5 M','DAL',76,11.80,4000000,82,6,7.19,0.833,83.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Devonte'' Graham','$10-15 M','SAS',73,11.70,12100000,82,9,15.50,0.267,26.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Isaac Okoro','$5-10 M','CLE',76,11.70,8920795,82,6,13.69,0.380,38.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jordan Goodwin','< $5 M','WAS',62,11.68,1927896,82,20,7.19,0.830,83.000,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Isaiah Jackson','< $5 M','IND',63,11.66,2696280,82,19,7.19,0.826,82.600,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Kenrich Williams','$5-10 M','OKC',53,11.63,6175000,82,29,13.69,0.367,36.700,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Damion Lee','< $5 M','PHX',74,11.60,2528233,82,8,7.19,0.823,82.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Isaiah Stewart','$5-10 M','DET',50,11.55,5266713,82,32,13.69,0.354,35.400,'Normal',0.75,0.25),
	 ('Reggie Bullock','$10-15 M','DAL',78,11.50,11014080,82,4,15.50,0.244,24.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Thomas Bryant','< $5 M','DEN',59,11.44,2528233,82,23,7.19,0.820,82.000,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('Georges Niang','$5-10 M','PHI',78,11.40,8800000,82,4,13.69,0.329,32.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Shaedon Sharpe','$5-10 M','POR',80,11.40,6313800,82,2,13.69,0.329,32.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Cory Joseph','< $5 M','DET',62,11.22,2019706,82,20,7.19,0.816,81.600,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Jock Landale','$5-10 M','PHX',69,11.20,8000000,82,13,13.69,0.316,31.600,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Malaki Branham','< $5 M','SAS',66,11.20,3071880,82,16,7.19,0.813,81.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Luka Samanic','< $5 M','UTA',7,11.18,2066585,82,75,7.19,0.810,81.000,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Sam Hauser','< $5 M','BOS',80,11.10,1927896,82,2,7.19,0.807,80.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Joe Harris','$15-20 M','BKN',74,11.00,19928571,82,8,19.25,0.138,13.800,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Terrence Ross','< $5 M','PHX',64,10.94,1000000,82,18,7.19,0.803,80.300,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Obi Toppin','$5-10 M','NYK',67,10.90,6803012,82,15,13.69,0.304,30.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Marvin Bagley','$10-15 M','DET',42,10.88,12500000,82,40,15.50,0.222,22.200,'Normal',0.75,0.25),
	 ('Precious Achiuwa','< $5 M','TOR',55,10.84,4379527,82,27,7.19,0.800,80.000,'Normal',0.78000000000000000000,0.22000000000000000000),
	 ('Seth Curry','< $5 M','BKN',61,10.80,4000000,82,21,7.19,0.797,79.700,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Justise Winslow','< $5 M','POR',29,10.73,1000000,82,53,7.19,0.793,79.300,'Normal',0.75,0.25),
	 ('Andre Drummond','< $5 M','CHI',67,10.70,3360000,82,15,7.19,0.790,79.000,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Mark Williams','< $5 M','CHA',43,10.65,3908160,82,39,7.19,0.787,78.700,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Jalen Johnson','< $5 M','ATL',70,10.60,2925360,82,12,7.19,0.784,78.400,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Mike Muscala','< $5 M','BOS',63,10.53,3500000,82,19,7.19,0.780,78.000,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Aaron Wiggins','< $5 M','OKC',70,10.50,1836096,82,12,7.19,0.777,77.700,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Joe Ingles','$10-15 M','MIL',46,10.43,11000000,82,36,15.50,0.200,20.000,'Normal',0.75,0.25),
	 ('Cam Thomas','< $5 M','BKN',57,10.41,2240160,82,25,7.19,0.774,77.400,'Normal',0.82000000000000000000,0.18000000000000000000),
	 ('Lonnie Walker','< $5 M','LAL',56,10.40,2019706,82,26,7.19,0.770,77.000,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Doug McDermott','$10-15 M','SAS',64,10.37,13750000,82,18,15.50,0.178,17.800,'Bad Value',0.96000000000000000000,0.04000000000000000000),
	 ('Hamidou Diallo','< $5 M','DET',56,10.32,1000000,82,26,7.19,0.767,76.700,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Anthony Lamb','< $5 M','GSW',62,10.30,1000000,82,20,7.19,0.764,76.400,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Landry Shamet','$10-15 M','PHX',40,10.28,10250000,82,42,15.50,0.156,15.600,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Trendon Watford','< $5 M','POR',62,10.03,1836096,82,20,7.19,0.761,76.100,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Davion Mitchell','$5-10 M','SAC',80,10.00,5063640,82,2,13.69,0.291,29.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Terence Davis','< $5 M','SAC',64,9.79,1000000,82,18,7.19,0.757,75.700,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Jae''Sean Tate','$5-10 M','HOU',31,9.75,6500000,82,51,13.69,0.278,27.800,'Normal',0.75,0.25),
	 ('Taurean Prince','< $5 M','MIN',54,9.58,4516000,82,28,7.19,0.754,75.400,'Normal',0.76000000000000000000,0.24000000000000000000),
	 ('Jordan Nwora','< $5 M','IND',62,9.57,3000000,82,20,7.19,0.751,75.100,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Bismack Biyombo','< $5 M','PHX',61,9.54,1000000,82,21,7.19,0.748,74.800,'Normal',0.90000000000000000000,0.10000000000000000000),
	 ('Ricky Rubio','$5-10 M','CLE',33,9.53,6146342,82,49,13.69,0.266,26.600,'Normal',0.75,0.25),
	 ('Jae Crowder','< $5 M','MIL',18,9.38,2019706,82,64,7.19,0.741,74.100,'Normal',0.75,0.25),
	 ('Joshua Primo','< $5 M','SAS',4,9.38,4341600,82,78,7.19,0.741,74.100,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Oshae Brissett','< $5 M','IND',65,9.31,2165000,82,17,7.19,0.738,73.800,'Normal',0.98000000000000000000,0.02000000000000000000),
	 ('Aleksej Pokusevski','$5-10 M','OKC',34,9.23,5009633,82,48,13.69,0.253,25.300,'Normal',0.75,0.25),
	 ('Kemba Walker','< $5 M','DAL',9,9.15,1000000,82,73,7.19,0.734,73.400,'Normal',0.75,0.25),
	 ('Jeenathan Williams','< $5 M','POR',5,9.08,1000000,82,77,7.19,0.731,73.100,'Normal',0.75,0.25),
	 ('Ochai Agbaji','< $5 M','UTA',59,9.03,4114200,82,23,7.19,0.728,72.800,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('Derrick Jones','< $5 M','CHI',64,9.02,3360000,82,18,7.19,0.725,72.500,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Jacob Gilyard','< $5 M','MEM',1,9.00,1000000,82,81,7.19,0.718,71.800,'Normal',0.75,0.25),
	 ('Kendrick Nunn','< $5 M','WAS',70,9.00,1000000,82,12,7.19,0.718,71.800,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Matisse Thybulle','$10-15 M','POR',71,9.00,10500000,82,11,15.50,0.133,13.300,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Gary Harris','$10-15 M','ORL',48,8.93,13000000,82,34,15.50,0.111,11.100,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('David Roddy','< $5 M','MEM',70,8.90,2718240,82,12,7.19,0.711,71.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Wenyen Gabriel','< $5 M','LAL',68,8.90,1000000,82,14,7.19,0.711,71.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Theo Maledon','< $5 M','CHA',44,8.85,1000000,82,38,7.19,0.705,70.500,'Normal',0.75,0.25),
	 ('T.J. Warren','< $5 M','PHX',42,8.85,1000000,82,40,7.19,0.705,70.500,'Normal',0.75,0.25),
	 ('Mohamed Bamba','< $5 M','LAL',49,8.78,2019706,82,33,7.19,0.702,70.200,'Normal',0.75,0.25),
	 ('Robert Covington','$10-15 M','LAC',48,8.63,11692308,82,34,15.50,0.089,8.900,'Bad Value',0.75,0.25),
	 ('Cam Reddish','< $5 M','POR',40,8.55,2165000,82,42,7.19,0.692,69.200,'Normal',0.75,0.25),
	 ('Jay Huff','< $5 M','WAS',7,8.55,1000000,82,75,7.19,0.692,69.200,'Normal',0.75,0.25),
	 ('Ty Jerome','< $5 M','GSW',45,8.55,2439025,82,37,7.19,0.692,69.200,'Normal',0.75,0.25),
	 ('Chimezie Metu','< $5 M','SAC',66,8.50,2019706,82,16,7.19,0.689,68.900,'Normal',1.00000000000000000000,0.00000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Jordan McLaughlin','< $5 M','MIN',43,8.48,2320000,82,39,7.19,0.685,68.500,'Normal',0.75,0.25),
	 ('Jeremiah Robinson-Earl','< $5 M','OKC',43,8.40,1900000,82,39,7.19,0.682,68.200,'Normal',0.75,0.25),
	 ('Nickeil Alexander-Walker','< $5 M','MIN',59,8.34,4687500,82,23,7.19,0.679,67.900,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('Goran Dragic','< $5 M','MIL',58,8.32,1000000,82,24,7.19,0.675,67.500,'Normal',0.84000000000000000000,0.16000000000000000000),
	 ('Paul Reed','$5-10 M','PHI',69,8.30,7723000,82,13,13.69,0.241,24.100,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Charles Bassey','< $5 M','SAS',35,8.25,2600000,82,47,7.19,0.672,67.200,'Normal',0.75,0.25),
	 ('P.J. Tucker','$10-15 M','PHI',75,8.20,11014500,82,7,15.50,0.067,6.700,'Bad Value',1.00000000000000000000,0.00000000000000000000),
	 ('Jaden Hardy','< $5 M','DAL',48,8.18,1719864,82,34,7.19,0.666,66.600,'Normal',0.75,0.25),
	 ('Willy Hernangomez','< $5 M','NOP',38,8.18,2559942,82,44,7.19,0.666,66.600,'Normal',0.75,0.25),
	 ('Dario Saric','< $5 M','OKC',57,8.12,2019706,82,25,7.19,0.662,66.200,'Normal',0.82000000000000000000,0.18000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Daniel Theis','$5-10 M','IND',7,8.10,9108387,82,75,13.69,0.228,22.800,'Normal',0.75,0.25),
	 ('Luke Kornet','< $5 M','BOS',69,8.00,2413304,82,13,7.19,0.659,65.900,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Svi Mykhailiuk','< $5 M','CHA',32,7.95,1000000,82,50,7.19,0.656,65.600,'Normal',0.75,0.25),
	 ('Dyson Daniels','$5-10 M','NOP',59,7.91,5784120,82,23,13.69,0.215,21.500,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('Lamar Stevens','< $5 M','CLE',62,7.91,400000,82,20,7.19,0.652,65.200,'Normal',0.92000000000000000000,0.08000000000000000000),
	 ('Dean Wade','$5-10 M','CLE',44,7.88,5709877,82,38,13.69,0.203,20.300,'Normal',0.75,0.25),
	 ('Julian Champagnie','< $5 M','SAS',17,7.88,3000000,82,65,7.19,0.646,64.600,'Normal',0.75,0.25),
	 ('Maxi Kleber','$10-15 M','DAL',37,7.88,11000000,82,45,15.50,0.044,4.400,'Bad Value',0.75,0.25),
	 ('Saben Lee','< $5 M','PHX',25,7.88,1000000,82,57,7.19,0.646,64.600,'Normal',0.75,0.25),
	 ('Ish Wainright','< $5 M','PHX',60,7.83,1927896,82,22,7.19,0.643,64.300,'Normal',0.88000000000000000000,0.12000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Duane Washington','< $5 M','PHX',31,7.80,1000000,82,51,7.19,0.639,63.900,'Normal',0.75,0.25),
	 ('Will Barton','< $5 M','TOR',56,7.76,1000000,82,26,7.19,0.636,63.600,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('George Hill','< $5 M','IND',46,7.73,1000000,82,36,7.19,0.630,63.000,'Normal',0.75,0.25),
	 ('Jaylin Williams','< $5 M','OKC',49,7.73,2000000,82,33,7.19,0.630,63.000,'Normal',0.75,0.25),
	 ('Edmond Sumner','< $5 M','BKN',53,7.65,1000000,82,29,7.19,0.623,62.300,'Normal',0.75,0.25),
	 ('Gary Payton','$5-10 M','GSW',22,7.65,8715000,82,60,13.69,0.190,19.000,'Bad Value',0.75,0.25),
	 ('James Wiseman','$10-15 M','DET',45,7.65,12119440,82,37,15.50,0.022,2.200,'Bad Value',0.75,0.25),
	 ('Javonte Green','< $5 M','CHI',32,7.65,1000000,82,50,7.19,0.623,62.300,'Normal',0.75,0.25),
	 ('Chris Duarte','< $5 M','IND',46,7.58,4124400,82,36,7.19,0.620,62.000,'Normal',0.75,0.25),
	 ('Christian Koloko','< $5 M','TOR',58,7.48,1719864,82,24,7.19,0.616,61.600,'Normal',0.84000000000000000000,0.16000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Yuta Watanabe','< $5 M','BKN',58,7.39,2346614,82,24,7.19,0.613,61.300,'Normal',0.84000000000000000000,0.16000000000000000000),
	 ('Jeff Green','$5-10 M','DEN',56,7.36,9600000,82,26,13.69,0.177,17.700,'Bad Value',0.80000000000000000000,0.20000000000000000000),
	 ('Blake Griffin','< $5 M','BOS',41,7.35,1000000,82,41,7.19,0.607,60.700,'Normal',0.75,0.25),
	 ('Lindy Waters','< $5 M','OKC',41,7.35,1000000,82,41,7.19,0.607,60.700,'Normal',0.75,0.25),
	 ('Jonathan Isaac','$15-20 M','ORL',11,7.28,17400000,82,71,19.25,0.103,10.300,'Bad Value',0.75,0.25),
	 ('Rudy Gay','$5-10 M','UTA',56,7.28,6479000,82,26,13.69,0.165,16.500,'Bad Value',0.80000000000000000000,0.20000000000000000000),
	 ('Christian Braun','< $5 M','DEN',76,7.20,2949120,82,6,7.19,0.603,60.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jarrell Brantley','< $5 M','UTA',4,7.13,1000000,82,78,7.19,0.600,60.000,'Normal',0.75,0.25),
	 ('Aaron Holiday','< $5 M','ATL',63,7.05,2019706,82,19,7.19,0.593,59.300,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Montrezl Harrell','< $5 M','PHI',57,7.05,2019706,82,25,7.19,0.593,59.300,'Normal',0.82000000000000000000,0.18000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Goga Bitadze','< $5 M','ORL',38,6.98,2066585,82,44,7.19,0.587,58.700,'Normal',0.75,0.25),
	 ('Jamal Cain','< $5 M','MIA',18,6.98,1000000,82,64,7.19,0.587,58.700,'Normal',0.75,0.25),
	 ('JaMychal Green','< $5 M','GSW',57,6.97,1000000,82,25,7.19,0.584,58.400,'Normal',0.82000000000000000000,0.18000000000000000000),
	 ('Vlatko Cancar','< $5 M','DEN',60,6.86,2234359,82,22,7.19,0.580,58.000,'Normal',0.88000000000000000000,0.12000000000000000000),
	 ('Eugene Omoruyi','< $5 M','DET',40,6.83,1000000,82,42,7.19,0.570,57.000,'Normal',0.75,0.25),
	 ('Sandro Mamukelashvili','< $5 M','SAS',43,6.83,1000000,82,39,7.19,0.570,57.000,'Normal',0.75,0.25),
	 ('Stanley Johnson','< $5 M','SAS',30,6.83,1000000,82,52,7.19,0.570,57.000,'Normal',0.75,0.25),
	 ('Andre Iguodala','< $5 M','GSW',8,6.75,1000000,82,74,7.19,0.564,56.400,'Normal',0.75,0.25),
	 ('Darius Bazley','< $5 M','PHX',43,6.75,2019706,82,39,7.19,0.564,56.400,'Normal',0.75,0.25),
	 ('Otto Porter','$5-10 M','TOR',8,6.68,6300000,82,74,13.69,0.152,15.200,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Jared Butler','< $5 M','OKC',6,6.60,1000000,82,76,7.19,0.561,56.100,'Normal',0.75,0.25),
	 ('Kevin Knox','< $5 M','POR',63,6.58,3000000,82,19,7.19,0.557,55.700,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Isaiah Livers','< $5 M','DET',52,6.53,1836096,82,30,7.19,0.544,54.400,'Normal',0.75,0.25),
	 ('Miles McBride','< $5 M','NYK',64,6.53,1836096,82,18,7.19,0.544,54.400,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Ousmane Dieng','< $5 M','OKC',39,6.53,4798440,82,43,7.19,0.544,54.400,'Normal',0.75,0.25),
	 ('Quenton Jackson','< $5 M','WAS',9,6.53,1000000,82,73,7.19,0.544,54.400,'Normal',0.75,0.25),
	 ('Moses Moody','< $5 M','GSW',63,6.39,3918480,82,19,7.19,0.541,54.100,'Normal',0.94000000000000000000,0.06000000000000000000),
	 ('Luka Garza','< $5 M','MIN',28,6.38,1000000,82,54,7.19,0.531,53.100,'Normal',0.75,0.25),
	 ('Romeo Langford','< $5 M','SAS',43,6.38,1000000,82,39,7.19,0.531,53.100,'Normal',0.75,0.25),
	 ('Sam Merrill','< $5 M','CLE',5,6.38,1997238,82,77,7.19,0.531,53.100,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Thaddeus Young','$5-10 M','TOR',54,6.23,8000000,82,28,13.69,0.139,13.900,'Bad Value',0.76000000000000000000,0.24000000000000000000),
	 ('Xavier Cooks','< $5 M','WAS',10,6.23,1719864,82,72,7.19,0.528,52.800,'Normal',0.75,0.25),
	 ('Nassir Little','$5-10 M','POR',54,6.16,6250000,82,28,13.69,0.127,12.700,'Bad Value',0.76000000000000000000,0.24000000000000000000),
	 ('Cody Martin','$5-10 M','CHA',7,6.15,7560000,82,75,13.69,0.101,10.100,'Bad Value',0.75,0.25),
	 ('Evan Fournier','$15-20 M','NYK',27,6.15,18857143,82,55,19.25,0.069,6.900,'Bad Value',0.75,0.25),
	 ('Kira Lewis','$5-10 M','NOP',25,6.15,5722116,82,57,13.69,0.101,10.100,'Bad Value',0.75,0.25),
	 ('Orlando Robinson','< $5 M','MIA',31,6.15,1801769,82,51,7.19,0.525,52.500,'Normal',0.75,0.25),
	 ('Josh Christopher','< $5 M','HOU',64,6.14,2485200,82,18,7.19,0.521,52.100,'Normal',0.96000000000000000000,0.04000000000000000000),
	 ('Derrick Rose','< $5 M','NYK',27,6.08,3196448,82,55,7.19,0.518,51.800,'Normal',0.75,0.25),
	 ('Johnny Davis','$5-10 M','WAS',28,6.00,5050800,82,54,13.69,0.089,8.900,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Payton Pritchard','< $5 M','BOS',48,6.00,4037277,82,34,7.19,0.515,51.500,'Normal',0.75,0.25),
	 ('Duncan Robinson','$15-20 M','MIA',42,5.85,18154000,82,40,19.25,0.034,3.400,'Bad Value',0.75,0.25),
	 ('Olivier Sarr','< $5 M','OKC',9,5.85,1000000,82,73,7.19,0.508,50.800,'Normal',0.75,0.25),
	 ('Patty Mills','$5-10 M','BKN',40,5.85,6802950,82,42,13.69,0.076,7.600,'Bad Value',0.75,0.25),
	 ('Rodney McGruder','< $5 M','DET',33,5.85,1000000,82,49,7.19,0.508,50.800,'Normal',0.75,0.25),
	 ('Chuma Okeke','$5-10 M','ORL',27,5.78,5266713,82,55,13.69,0.063,6.300,'Bad Value',0.75,0.25),
	 ('R.J. Hampton','< $5 M','DET',47,5.78,1000000,82,35,7.19,0.505,50.500,'Normal',0.75,0.25),
	 ('Cody Zeller','< $5 M','MIA',15,5.70,2019706,82,67,7.19,0.498,49.800,'Normal',0.75,0.25),
	 ('Day''Ron Sharpe','< $5 M','BKN',48,5.70,2210040,82,34,7.19,0.498,49.800,'Normal',0.75,0.25),
	 ('Brandon Boston','< $5 M','LAC',22,5.63,1836096,82,60,7.19,0.489,48.900,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('DeAndre Jordan','< $5 M','DEN',39,5.63,2019706,82,43,7.19,0.489,48.900,'Normal',0.75,0.25),
	 ('Stanley Umude','< $5 M','DET',1,5.63,1000000,82,81,7.19,0.489,48.900,'Normal',0.75,0.25),
	 ('Usman Garuba','< $5 M','HOU',75,5.60,2588400,82,7,7.19,0.485,48.500,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jaxson Hayes','< $5 M','NOP',47,5.55,2165000,82,35,7.19,0.479,47.900,'Normal',0.75,0.25),
	 ('TyTy Washington','< $5 M','HOU',31,5.55,2320440,82,51,7.19,0.479,47.900,'Normal',0.75,0.25),
	 ('Dalano Banton','< $5 M','TOR',31,5.48,2019706,82,51,7.19,0.475,47.500,'Normal',0.75,0.25),
	 ('Haywood Highsmith','< $5 M','MIA',54,5.40,1902137,82,28,7.19,0.462,46.200,'Normal',0.76000000000000000000,0.24000000000000000000),
	 ('Malachi Flynn','< $5 M','TOR',53,5.40,3873025,82,29,7.19,0.462,46.200,'Normal',0.75,0.25),
	 ('Moses Brown','< $5 M','BKN',36,5.40,1000000,82,46,7.19,0.462,46.200,'Normal',0.75,0.25),
	 ('Nikola Jovic','< $5 M','MIA',15,5.40,2352000,82,67,7.19,0.462,46.200,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Danuel House','< $5 M','PHI',56,5.36,4310250,82,26,7.19,0.459,45.900,'Normal',0.80000000000000000000,0.20000000000000000000),
	 ('Austin Rivers','< $5 M','MIN',52,5.33,1000000,82,30,7.19,0.456,45.600,'Normal',0.75,0.25),
	 ('Bruno Fernando','< $5 M','ATL',39,5.25,2581522,82,43,7.19,0.449,44.900,'Normal',0.75,0.25),
	 ('Trevelin Queen','< $5 M','IND',7,5.25,1000000,82,75,7.19,0.449,44.900,'Normal',0.75,0.25),
	 ('Dewayne Dedmon','$5-10 M','PHI',38,5.18,7072674,82,44,13.69,0.051,5.100,'Bad Value',0.75,0.25),
	 ('Zeke Nnaji','< $5 M','DEN',52,5.18,4306281,82,30,7.19,0.446,44.600,'Normal',0.75,0.25),
	 ('James Bouknight','< $5 M','CHA',34,5.10,4570080,82,48,7.19,0.433,43.300,'Normal',0.75,0.25),
	 ('Jarrett Culver','< $5 M','ATL',10,5.10,1000000,82,72,7.19,0.433,43.300,'Normal',0.75,0.25),
	 ('Omer Yurtseven','< $5 M','MIA',9,5.10,2800000,82,73,7.19,0.433,43.300,'Normal',0.75,0.25),
	 ('Wesley Matthews','< $5 M','MIL',52,5.10,2019706,82,30,7.19,0.433,43.300,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Ziaire Williams','< $5 M','MEM',37,5.03,4810200,82,45,7.19,0.430,43.000,'Normal',0.75,0.25),
	 ('Dru Smith','< $5 M','BKN',15,4.95,1000000,82,67,7.19,0.426,42.600,'Normal',0.75,0.25),
	 ('Daishen Nix','< $5 M','HOU',57,4.92,1000000,82,25,7.19,0.423,42.300,'Normal',0.82000000000000000000,0.18000000000000000000),
	 ('Carlik Jones','< $5 M','CHI',7,4.88,1927896,82,75,7.19,0.413,41.300,'Normal',0.75,0.25),
	 ('Danny Green','< $5 M','CLE',11,4.88,1000000,82,71,7.19,0.413,41.300,'Normal',0.75,0.25),
	 ('Raul Neto','< $5 M','CLE',48,4.88,1000000,82,34,7.19,0.413,41.300,'Normal',0.75,0.25),
	 ('Blake Wesley','< $5 M','SAS',37,4.80,2504640,82,45,7.19,0.403,40.300,'Normal',0.75,0.25),
	 ('Dominick Barlow','< $5 M','SAS',28,4.80,1000000,82,54,7.19,0.403,40.300,'Normal',0.75,0.25),
	 ('JT Thor','< $5 M','CHA',69,4.80,1836096,82,13,7.19,0.403,40.300,'Normal',1.00000000000000000000,0.00000000000000000000),
	 ('Jericho Sims','< $5 M','NYK',52,4.73,1927896,82,30,7.19,0.393,39.300,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Kevon Harris','< $5 M','ORL',34,4.73,1000000,82,48,7.19,0.393,39.300,'Normal',0.75,0.25),
	 ('Markieff Morris','< $5 M','DAL',35,4.73,1000000,82,47,7.19,0.393,39.300,'Normal',0.75,0.25),
	 ('Josh Minott','< $5 M','MIN',15,4.65,1719864,82,67,7.19,0.387,38.700,'Normal',0.75,0.25),
	 ('McKinley Wright','< $5 M','DAL',27,4.65,1000000,82,55,7.19,0.387,38.700,'Normal',0.75,0.25),
	 ('Kenneth Lofton','< $5 M','MEM',24,4.58,1719864,82,58,7.19,0.377,37.700,'Normal',0.75,0.25),
	 ('MarJon Beauchamp','< $5 M','MIL',52,4.58,2609400,82,30,7.19,0.377,37.700,'Normal',0.75,0.25),
	 ('Simone Fontecchio','< $5 M','UTA',52,4.58,3044872,82,30,7.19,0.377,37.700,'Normal',0.75,0.25),
	 ('Anthony Gill','< $5 M','WAS',59,4.56,1997238,82,23,7.19,0.374,37.400,'Normal',0.86000000000000000000,0.14000000000000000000),
	 ('Bryce McGowens','< $5 M','CHA',46,4.50,1719864,82,36,7.19,0.370,37.000,'Normal',0.75,0.25),
	 ('Davis Bertans','$15-20 M','DAL',45,4.50,17000000,82,37,19.25,0.000,0.000,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Garrison Mathews','< $5 M','ATL',54,4.48,2000000,82,28,7.19,0.367,36.700,'Normal',0.76000000000000000000,0.24000000000000000000),
	 ('Jared Rhoden','< $5 M','DET',14,4.43,1000000,82,68,7.19,0.348,34.800,'Normal',0.75,0.25),
	 ('Juancho Hernangomez','< $5 M','TOR',42,4.43,1000000,82,40,7.19,0.348,34.800,'Normal',0.75,0.25),
	 ('Justin Holiday','< $5 M','DAL',46,4.43,2019706,82,36,7.19,0.348,34.800,'Normal',0.75,0.25),
	 ('Kai Jones','< $5 M','CHA',46,4.43,3047880,82,36,7.19,0.348,34.800,'Normal',0.75,0.25),
	 ('Lindell Wigginton','< $5 M','MIL',7,4.43,1000000,82,75,7.19,0.348,34.800,'Normal',0.75,0.25),
	 ('Taj Gibson','< $5 M','WAS',48,4.43,1000000,82,34,7.19,0.348,34.800,'Normal',0.75,0.25),
	 ('Frank Ntilikina','< $5 M','DAL',47,4.35,1000000,82,35,7.19,0.344,34.400,'Normal',0.75,0.25),
	 ('Isaiah Mobley','< $5 M','CLE',13,4.28,1000000,82,69,7.19,0.341,34.100,'Normal',0.75,0.25),
	 ('JaVale McGee','$5-10 M','DAL',42,4.20,5734280,82,40,13.69,0.038,3.800,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('A.J. Green','< $5 M','MIL',35,4.13,1901769,82,47,7.19,0.321,32.100,'Normal',0.75,0.25),
	 ('Boban Marjanovic','< $5 M','HOU',31,4.13,1000000,82,51,7.19,0.321,32.100,'Normal',0.75,0.25),
	 ('Darius Days','< $5 M','HOU',4,4.13,1000000,82,78,7.19,0.321,32.100,'Normal',0.75,0.25),
	 ('Isaiah Roby','< $5 M','SAS',42,4.13,1000000,82,40,7.19,0.321,32.100,'Normal',0.75,0.25),
	 ('James Johnson','< $5 M','IND',18,4.13,1000000,82,64,7.19,0.321,32.100,'Normal',0.75,0.25),
	 ('Jeff Dowtin','< $5 M','TOR',25,4.13,2019706,82,57,7.19,0.321,32.100,'Normal',0.75,0.25),
	 ('Gorgui Dieng','< $5 M','SAS',31,4.05,1000000,82,51,7.19,0.311,31.100,'Normal',0.75,0.25),
	 ('Ish Smith','< $5 M','DEN',43,4.05,1000000,82,39,7.19,0.311,31.100,'Normal',0.75,0.25),
	 ('Jason Preston','< $5 M','LAC',14,4.05,1000000,82,68,7.19,0.311,31.100,'Normal',0.75,0.25),
	 ('Jabari Walker','< $5 M','POR',56,4.00,1719864,82,26,7.19,0.308,30.800,'Normal',0.80000000000000000000,0.20000000000000000000);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Admiral Schofield','< $5 M','ORL',37,3.98,1000000,82,45,7.19,0.305,30.500,'Normal',0.75,0.25),
	 ('Keon Johnson','< $5 M','POR',40,3.90,2808720,82,42,7.19,0.295,29.500,'Normal',0.75,0.25),
	 ('Kessler Edwards','< $5 M','SAC',35,3.90,1927896,82,47,7.19,0.295,29.500,'Normal',0.75,0.25),
	 ('Serge Ibaka','< $5 M','MIL',16,3.90,1000000,82,66,7.19,0.295,29.500,'Normal',0.75,0.25),
	 ('Damian Jones','< $5 M','UTA',41,3.83,2586665,82,41,7.19,0.289,28.900,'Normal',0.75,0.25),
	 ('Micah Potter','< $5 M','UTA',7,3.83,1000000,82,75,7.19,0.289,28.900,'Normal',0.75,0.25),
	 ('Caleb Houstan','< $5 M','ORL',51,3.75,2000000,82,31,7.19,0.279,27.900,'Normal',0.75,0.25),
	 ('Furkan Korkmaz','$5-10 M','PHI',37,3.75,5370370,82,45,13.69,0.025,2.500,'Bad Value',0.75,0.25),
	 ('Justin Minaya','< $5 M','POR',3,3.75,1000000,82,79,7.19,0.279,27.900,'Normal',0.75,0.25),
	 ('Matt Ryan','< $5 M','MIN',34,3.75,1000000,82,48,7.19,0.279,27.900,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Udoka Azubuike','< $5 M','UTA',36,3.68,1000000,82,46,7.19,0.275,27.500,'Normal',0.75,0.25),
	 ('Jordan Schakel','< $5 M','WAS',2,3.60,1000000,82,80,7.19,0.266,26.600,'Normal',0.75,0.25),
	 ('Meyers Leonard','< $5 M','MIL',9,3.60,1000000,82,73,7.19,0.266,26.600,'Normal',0.75,0.25),
	 ('Nathan Knight','< $5 M','MIN',38,3.60,1000000,82,44,7.19,0.266,26.600,'Normal',0.75,0.25),
	 ('David Duke','< $5 M','BKN',23,3.53,1000000,82,59,7.19,0.246,24.600,'Normal',0.75,0.25),
	 ('Facundo Campazzo','< $5 M','DAL',8,3.53,1000000,82,74,7.19,0.246,24.600,'Normal',0.75,0.25),
	 ('Jaden Springer','< $5 M','PHI',16,3.53,2226240,82,66,7.19,0.246,24.600,'Normal',0.75,0.25),
	 ('Johnny Juzang','< $5 M','UTA',18,3.53,1000000,82,64,7.19,0.246,24.600,'Normal',0.75,0.25),
	 ('Juan Toscano-Anderson','< $5 M','UTA',52,3.53,1000000,82,30,7.19,0.246,24.600,'Normal',0.75,0.25),
	 ('Kennedy Chandler','< $5 M','MEM',36,3.53,1719864,82,46,7.19,0.246,24.600,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Ron Harper','< $5 M','TOR',9,3.45,1000000,82,73,7.19,0.243,24.300,'Normal',0.75,0.25),
	 ('Frank Kaminsky','< $5 M','HOU',37,3.38,1000000,82,45,7.19,0.233,23.300,'Normal',0.75,0.25),
	 ('Jay Scrubb','< $5 M','ORL',2,3.38,1000000,82,80,7.19,0.233,23.300,'Normal',0.75,0.25),
	 ('Terry Taylor','< $5 M','CHI',31,3.38,1000000,82,51,7.19,0.233,23.300,'Normal',0.75,0.25),
	 ('Amir Coffey','< $5 M','LAC',50,3.23,3666667,82,32,7.19,0.220,22.000,'Normal',0.75,0.25),
	 ('Dalen Terry','< $5 M','CHI',38,3.23,3350760,82,44,7.19,0.220,22.000,'Normal',0.75,0.25),
	 ('Jamaree Bouyea','< $5 M','WAS',5,3.23,1000000,82,77,7.19,0.220,22.000,'Normal',0.75,0.25),
	 ('Patrick Baldwin','< $5 M','GSW',31,3.23,2337720,82,51,7.19,0.220,22.000,'Normal',0.75,0.25),
	 ('Justin Champagnie','< $5 M','BOS',5,3.15,1000000,82,77,7.19,0.203,20.300,'Normal',0.75,0.25),
	 ('Max Christie','< $5 M','LAL',41,3.15,1719864,82,41,7.19,0.203,20.300,'Normal',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Moussa Diabate','< $5 M','LAC',22,3.15,1000000,82,60,7.19,0.203,20.300,'Normal',0.75,0.25),
	 ('Peyton Watson','< $5 M','DEN',23,3.15,2303520,82,59,7.19,0.203,20.300,'Normal',0.75,0.25),
	 ('Theo Pinson','< $5 M','DAL',40,3.15,1000000,82,42,7.19,0.203,20.300,'Normal',0.75,0.25),
	 ('Trent Forrest','< $5 M','ATL',23,3.08,1000000,82,59,7.19,0.200,20.000,'Normal',0.75,0.25),
	 ('Alex Len','< $5 M','SAC',26,3.00,2019706,82,56,7.19,0.184,18.400,'Bad Value',0.75,0.25),
	 ('Devon Dotson','< $5 M','WAS',6,3.00,1000000,82,76,7.19,0.184,18.400,'Bad Value',0.75,0.25),
	 ('Donovan Williams','< $5 M','ATL',2,3.00,1000000,82,80,7.19,0.184,18.400,'Bad Value',0.75,0.25),
	 ('Mamadi Diakite','< $5 M','CLE',22,3.00,1000000,82,60,7.19,0.184,18.400,'Bad Value',0.75,0.25),
	 ('Nerlens Noel','< $5 M','BKN',17,3.00,300000,82,65,7.19,0.184,18.400,'Bad Value',0.75,0.25),
	 ('Alize Johnson','< $5 M','SAS',4,2.93,1000000,82,78,7.19,0.174,17.400,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Bryn Forbes','< $5 M','MIN',25,2.93,1000000,82,57,7.19,0.174,17.400,'Bad Value',0.75,0.25),
	 ('Kendall Brown','< $5 M','IND',6,2.93,1000000,82,76,7.19,0.174,17.400,'Bad Value',0.75,0.25),
	 ('Khem Birch','$5-10 M','TOR',20,2.93,6985000,82,62,13.69,0.013,1.300,'Bad Value',0.75,0.25),
	 ('Jake LaRavia','< $5 M','MEM',35,2.85,3199920,82,47,7.19,0.164,16.400,'Bad Value',0.75,0.25),
	 ('Jordan Hall','< $5 M','SAS',9,2.85,1000000,82,73,7.19,0.164,16.400,'Bad Value',0.75,0.25),
	 ('Michael Carter-Williams','< $5 M','ORL',4,2.85,1000000,82,78,7.19,0.164,16.400,'Bad Value',0.75,0.25),
	 ('Richaun Holmes','$10-15 M','SAC',42,2.78,12046020,82,40,15.50,0.000,0.000,'Bad Value',0.75,0.25),
	 ('Tyler Dorsey','< $5 M','DAL',3,2.78,1000000,82,79,7.19,0.157,15.700,'Bad Value',0.75,0.25),
	 ('Udonis Haslem','< $5 M','MIA',7,2.78,1000000,82,75,7.19,0.157,15.700,'Bad Value',0.75,0.25),
	 ('Scotty Pippen','< $5 M','LAL',6,2.70,1000000,82,76,7.19,0.154,15.400,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Garrett Temple','$5-10 M','NOP',25,2.55,5401000,82,57,13.69,0.000,0.000,'Bad Value',0.75,0.25),
	 ('John Butler','< $5 M','POR',19,2.55,1000000,82,63,7.19,0.151,15.100,'Bad Value',0.75,0.25),
	 ('JD Davison','< $5 M','BOS',12,2.40,1000000,82,70,7.19,0.144,14.400,'Bad Value',0.75,0.25),
	 ('Robin Lopez','< $5 M','CLE',37,2.40,2019706,82,45,7.19,0.144,14.400,'Bad Value',0.75,0.25),
	 ('A.J. Lawson','< $5 M','DAL',15,2.33,1000000,82,67,7.19,0.138,13.800,'Bad Value',0.75,0.25),
	 ('Buddy Boeheim','< $5 M','DET',10,2.33,1000000,82,72,7.19,0.138,13.800,'Bad Value',0.75,0.25),
	 ('Greg Brown','< $5 M','POR',16,2.25,1000000,82,66,7.19,0.128,12.800,'Bad Value',0.75,0.25),
	 ('Lester Quinones','< $5 M','GSW',4,2.25,1000000,82,78,7.19,0.128,12.800,'Bad Value',0.75,0.25),
	 ('Xavier Moon','< $5 M','LAC',4,2.25,1000000,82,78,7.19,0.128,12.800,'Bad Value',0.75,0.25),
	 ('Matthew Dellavedova','< $5 M','SAC',32,2.10,1000000,82,50,7.19,0.115,11.500,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Mfiondu Kabengele','< $5 M','BOS',4,2.10,1000000,82,78,7.19,0.115,11.500,'Bad Value',0.75,0.25),
	 ('Sterling Brown','< $5 M','LAL',4,2.10,1000000,82,78,7.19,0.115,11.500,'Bad Value',0.75,0.25),
	 ('Tony Bradley','< $5 M','CHI',12,2.10,1000000,82,70,7.19,0.115,11.500,'Bad Value',0.75,0.25),
	 ('Cole Swider','< $5 M','LAL',7,2.03,1000000,82,75,7.19,0.098,9.800,'Bad Value',0.75,0.25),
	 ('Isaiah Todd','< $5 M','WAS',6,2.03,1836096,82,76,7.19,0.098,9.800,'Bad Value',0.75,0.25),
	 ('KZ Okpala','< $5 M','SAC',35,2.03,1000000,82,47,7.19,0.098,9.800,'Bad Value',0.75,0.25),
	 ('Trevor Hudgins','< $5 M','HOU',5,2.03,1000000,82,77,7.19,0.098,9.800,'Bad Value',0.75,0.25),
	 ('Vit Krejci','< $5 M','ATL',29,2.03,1000000,82,53,7.19,0.098,9.800,'Bad Value',0.75,0.25),
	 ('Davon Reed','< $5 M','LAL',43,1.95,1000000,82,39,7.19,0.092,9.200,'Bad Value',0.75,0.25),
	 ('Xavier Sneed','< $5 M','CHA',4,1.95,1000000,82,78,7.19,0.092,9.200,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Noah Vonleh','< $5 M','BOS',23,1.88,1000000,82,59,7.19,0.089,8.900,'Bad Value',0.75,0.25),
	 ('PJ Dozier','< $5 M','SAC',16,1.80,1000000,82,66,7.19,0.082,8.200,'Bad Value',0.75,0.25),
	 ('Ryan Arcidiacono','< $5 M','POR',20,1.80,1000000,82,62,7.19,0.082,8.200,'Bad Value',0.75,0.25),
	 ('Keon Ellis','< $5 M','SAC',16,1.73,1000000,82,66,7.19,0.072,7.200,'Bad Value',0.75,0.25),
	 ('Vince Williams','< $5 M','MEM',15,1.73,1000000,82,67,7.19,0.072,7.200,'Bad Value',0.75,0.25),
	 ('Wendell Moore','< $5 M','MIN',29,1.73,2421720,82,53,7.19,0.072,7.200,'Bad Value',0.75,0.25),
	 ('Dylan Windler','< $5 M','CLE',3,1.65,1000000,82,79,7.19,0.066,6.600,'Bad Value',0.75,0.25),
	 ('Malcolm Hill','< $5 M','CHI',5,1.65,1000000,82,77,7.19,0.066,6.600,'Bad Value',0.75,0.25),
	 ('Marko Simonovic','< $5 M','CHI',7,1.58,1000000,82,75,7.19,0.062,6.200,'Bad Value',0.75,0.25),
	 ('Jack White','< $5 M','DEN',17,1.50,1801769,82,65,7.19,0.059,5.900,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Dereon Seabron','< $5 M','NOP',5,1.43,1000000,82,77,7.19,0.056,5.600,'Bad Value',0.75,0.25),
	 ('Tyrese Martin','< $5 M','ATL',16,1.35,1000000,82,66,7.19,0.052,5.200,'Bad Value',0.75,0.25),
	 ('Joe Wieskamp','< $5 M','TOR',9,1.28,1000000,82,73,7.19,0.049,4.900,'Bad Value',0.75,0.25),
	 ('Frank Jackson','< $5 M','UTA',1,1.13,1000000,82,81,7.19,0.039,3.900,'Bad Value',0.75,0.25),
	 ('Kobi Simmons','< $5 M','CHA',5,1.13,1000000,82,77,7.19,0.039,3.900,'Bad Value',0.75,0.25),
	 ('Vernon Carey','< $5 M','WAS',11,1.13,1000000,82,71,7.19,0.039,3.900,'Bad Value',0.75,0.25),
	 ('Deonte Burton','< $5 M','SAC',2,0.98,1000000,82,80,7.19,0.030,3.000,'Bad Value',0.75,0.25),
	 ('Leandro Bolmaro','< $5 M','UTA',14,0.98,1000000,82,68,7.19,0.030,3.000,'Bad Value',0.75,0.25),
	 ('Neemias Queta','< $5 M','SAC',5,0.98,250000,82,77,7.19,0.030,3.000,'Bad Value',0.75,0.25),
	 ('Braxton Key','< $5 M','DET',3,0.75,1000000,82,79,7.19,0.023,2.300,'Bad Value',0.75,0.25);
INSERT INTO contract_value_analysis (player,salary_rank,team,games_played,player_mvp_calc_avg,salary,team_games_played,games_missed,pvm_rank,rankingish,percentile_rank,color_var,adj_penalty_final,pct_penalized) VALUES
	 ('Chris Silva','< $5 M','DAL',1,0.75,1000000,82,81,7.19,0.023,2.300,'Bad Value',0.75,0.25),
	 ('Thanasis Antetokounmpo','< $5 M','MIL',37,0.68,1000000,82,45,7.19,0.020,2.000,'Bad Value',0.75,0.25),
	 ('Justin Jackson','< $5 M','BOS',23,0.60,1000000,82,59,7.19,0.016,1.600,'Bad Value',0.75,0.25),
	 ('Ryan Rollins','< $5 M','GSW',12,-0.38,1719864,82,70,7.19,0.013,1.300,'Bad Value',0.75,0.25),
	 ('Michael Foster','< $5 M','PHI',1,-0.75,1000000,82,81,7.19,0.010,1.000,'Bad Value',0.75,0.25),
	 ('Chima Moneke','< $5 M','SAC',2,-1.13,1000000,82,80,7.19,0.007,0.700,'Bad Value',0.75,0.25),
	 ('Trevor Keels','< $5 M','NYK',3,-1.28,1000000,82,79,7.19,0.003,0.300,'Bad Value',0.75,0.25),
	 ('Alondes Williams','< $5 M','BKN',1,-3.75,1000000,82,81,7.19,0.000,0.000,'Bad Value',0.75,0.25);


DROP TABLE IF EXISTS pbp;
CREATE TABLE IF NOT EXISTS pbp
(
    time_quarter text COLLATE pg_catalog."default",
    play text COLLATE pg_catalog."default",
    time_remaining_final numeric,
    quarter text COLLATE pg_catalog."default",
    away_score text COLLATE pg_catalog."default",
    score text COLLATE pg_catalog."default",
    home_score text COLLATE pg_catalog."default",
    home_team text COLLATE pg_catalog."default",
    away_team text COLLATE pg_catalog."default",
    score_away numeric,
    score_home numeric,
    margin_score numeric,
    date date,
    leading_team text COLLATE pg_catalog."default",
    home_team_full text COLLATE pg_catalog."default",
    home_primary_color text COLLATE pg_catalog."default",
    away_team_full text COLLATE pg_catalog."default",
    away_primary_color text COLLATE pg_catalog."default",
    game_description text COLLATE pg_catalog."default",
    away_fill text COLLATE pg_catalog."default",
    home_fill text COLLATE pg_catalog."default",
    scoring_team_color text COLLATE pg_catalog."default",
    scoring_team text COLLATE pg_catalog."default",
    max_home_lead numeric,
    max_away_lead numeric,
    winning_team text COLLATE pg_catalog."default",
    losing_team text COLLATE pg_catalog."default"
);

INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('12:00','Jump ball: B. Adebayo vs. N. Jokić (J. Murray gains possession)',48.00,'1st Quarter','Jump ball: B. Adebayo vs. N. Jokić (J. Murray gains possession)','Jump ball: B. Adebayo vs. N. Jokić (J. Murray gains possession)','Jump ball: B. Adebayo vs. N. Jokić (J. Murray gains possession)','DEN','MIA',0,0,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('11:39','B. Adebayo makes 2-pt dunk from 2 ft',47.65,'1st Quarter','+2','2-0',NULL,'DEN','MIA',2,0,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('10:35','M. Strus makes 3-pt jump shot from 27 ft (assist by G. Vincent)',46.58,'1st Quarter','+3','5-0',NULL,'DEN','MIA',5,0,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('10:00','K. Caldwell-Pope makes 2-pt jump shot from 15 ft',46.00,'1st Quarter',NULL,'5-2','+2','DEN','MIA',5,2,-3,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('8:15','K. Caldwell-Pope makes 2-pt jump shot from 9 ft (assist by J. Murray)',44.25,'1st Quarter',NULL,'5-4','+2','DEN','MIA',5,4,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('7:48','A. Gordon makes 2-pt jump shot from 10 ft',43.80,'1st Quarter',NULL,'5-6','+2','DEN','MIA',5,6,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('6:47','J. Murray makes 2-pt dunk from 2 ft',42.78,'1st Quarter',NULL,'5-8','+2','DEN','MIA',5,8,3,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('6:18','M. Porter makes 2-pt jump shot from 12 ft (assist by N. Jokić)',42.30,'1st Quarter',NULL,'5-10','+2','DEN','MIA',5,10,5,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('5:57','J. Green makes 2-pt dunk from 2 ft (assist by M. Porter)',41.95,'1st Quarter',NULL,'5-12','+2','DEN','MIA',5,12,7,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('5:41','M. Strus makes 2-pt layup from 4 ft (assist by J. Butler)',41.68,'1st Quarter','+2','7-12',NULL,'DEN','MIA',7,12,5,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('5:41','M. Strus makes free throw 1 of 1',41.68,'1st Quarter','+1','8-12',NULL,'DEN','MIA',8,12,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('5:28','N. Jokić makes 3-pt jump shot from 26 ft (assist by J. Green)',41.47,'1st Quarter',NULL,'8-15','+3','DEN','MIA',8,15,7,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('4:55','M. Porter makes free throw 2 of 2',40.92,'1st Quarter',NULL,'8-16','+1','DEN','MIA',8,16,8,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('4:42','B. Adebayo makes 2-pt dunk from 1 ft (assist by M. Strus)',40.70,'1st Quarter','+2','10-16',NULL,'DEN','MIA',10,16,6,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('4:11','C. Martin makes 2-pt layup from 2 ft (assist by K. Lowry)',40.18,'1st Quarter','+2','12-16',NULL,'DEN','MIA',12,16,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:46','M. Strus makes 2-pt dunk from 3 ft (assist by K. Lowry)',39.77,'1st Quarter','+2','14-16',NULL,'DEN','MIA',14,16,2,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:27','J. Green makes 2-pt layup from 3 ft (assist by N. Jokić)',39.45,'1st Quarter',NULL,'14-18','+2','DEN','MIA',14,18,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('3:15','B. Adebayo makes 2-pt jump shot from 9 ft (assist by K. Lowry)',39.25,'1st Quarter','+2','16-18',NULL,'DEN','MIA',16,18,2,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('2:42','B. Adebayo makes free throw 1 of 1',38.70,'1st Quarter','+1','19-18',NULL,'DEN','MIA',19,18,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('2:42','B. Adebayo makes 2-pt layup from 2 ft',38.70,'1st Quarter','+2','18-18',NULL,'DEN','MIA',18,18,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('2:14','B. Adebayo makes 2-pt jump shot from 7 ft',38.23,'1st Quarter','+2','21-18',NULL,'DEN','MIA',21,18,-3,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('2:14','B. Adebayo makes free throw 1 of 1',38.23,'1st Quarter','+1','22-18',NULL,'DEN','MIA',22,18,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('1:09','M. Porter makes 2-pt layup from 2 ft',37.15,'1st Quarter',NULL,'22-20','+2','DEN','MIA',22,20,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:39','M. Porter makes 2-pt jump shot from 11 ft (assist by J. Murray)',36.65,'1st Quarter',NULL,'22-22','+2','DEN','MIA',22,22,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:21','B. Adebayo makes 2-pt hook shot at rim',36.35,'1st Quarter','+2','24-22',NULL,'DEN','MIA',24,22,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('0:00','End of 1st quarter',36.00,'1st Quarter','End of 1st quarter','End of 1st quarter','End of 1st quarter','DEN','MIA',24,22,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('12:00','Start of 2nd quarter',36.00,'2nd Quarter','Start of 2nd quarter','Start of 2nd quarter','Start of 2nd quarter','DEN','MIA',24,22,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('11:39','J. Butler makes 2-pt layup from 3 ft',35.65,'2nd Quarter','+2','26-22',NULL,'DEN','MIA',26,22,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('11:13','J. Butler makes free throw 2 of 2',35.22,'2nd Quarter','+1','28-22',NULL,'DEN','MIA',28,22,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('11:13','J. Butler makes free throw 1 of 2',35.22,'2nd Quarter','+1','27-22',NULL,'DEN','MIA',27,22,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('10:17','A. Gordon makes free throw 2 of 2',34.28,'2nd Quarter',NULL,'28-23','+1','DEN','MIA',28,23,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('9:59','C. Braun makes 2-pt layup from 3 ft (assist by M. Porter)',33.98,'2nd Quarter',NULL,'28-25','+2','DEN','MIA',28,25,-3,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('9:46','J. Butler makes free throw 2 of 2',33.77,'2nd Quarter','+1','30-25',NULL,'DEN','MIA',30,25,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('9:46','J. Butler makes free throw 1 of 2',33.77,'2nd Quarter','+1','29-25',NULL,'DEN','MIA',29,25,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('9:32','B. Brown makes 2-pt layup from 3 ft (assist by J. Murray)',33.53,'2nd Quarter',NULL,'30-27','+2','DEN','MIA',30,27,-3,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('9:09','C. Martin makes free throw 2 of 2',33.15,'2nd Quarter','+1','32-27',NULL,'DEN','MIA',32,27,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('9:09','C. Martin makes free throw 1 of 2',33.15,'2nd Quarter','+1','31-27',NULL,'DEN','MIA',31,27,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('8:22','C. Martin makes 2-pt layup from 5 ft',32.37,'2nd Quarter','+2','34-27',NULL,'DEN','MIA',34,27,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('8:04','N. Jokić makes 2-pt jump shot from 5 ft (assist by C. Braun)',32.07,'2nd Quarter',NULL,'34-29','+2','DEN','MIA',34,29,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('7:47','D. Robinson makes 3-pt jump shot from 24 ft (assist by J. Butler)',31.78,'2nd Quarter','+3','37-29',NULL,'DEN','MIA',37,29,-8,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('7:17','D. Robinson makes 2-pt layup from 3 ft (assist by B. Adebayo)',31.28,'2nd Quarter','+2','39-29',NULL,'DEN','MIA',39,29,-10,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('6:56','N. Jokić makes 2-pt layup from 3 ft',30.93,'2nd Quarter',NULL,'39-31','+2','DEN','MIA',39,31,-8,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('6:17','K. Caldwell-Pope makes 2-pt jump shot from 17 ft (assist by N. Jokić)',30.28,'2nd Quarter',NULL,'39-33','+2','DEN','MIA',39,33,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('5:46','B. Brown makes 2-pt dunk from 1 ft (assist by K. Caldwell-Pope)',29.77,'2nd Quarter',NULL,'39-35','+2','DEN','MIA',39,35,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('5:23','K. Lowry makes 3-pt jump shot from 23 ft',29.38,'2nd Quarter','+3','42-35',NULL,'DEN','MIA',42,35,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('5:00','N. Jokić makes 2-pt jump shot from 7 ft (assist by J. Murray)',29.00,'2nd Quarter',NULL,'42-37','+2','DEN','MIA',42,37,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('4:29','J. Murray makes 2-pt jump shot from 16 ft',28.48,'2nd Quarter',NULL,'42-39','+2','DEN','MIA',42,39,-3,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('4:14','K. Lowry makes 3-pt jump shot from 25 ft',28.23,'2nd Quarter','+3','45-39',NULL,'DEN','MIA',45,39,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:32','J. Butler makes 2-pt dunk from 1 ft',27.53,'2nd Quarter','+2','47-39',NULL,'DEN','MIA',47,39,-8,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('2:41','C. Braun makes 2-pt layup from 3 ft',26.68,'2nd Quarter',NULL,'47-41','+2','DEN','MIA',47,41,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('2:13','C. Braun makes free throw 1 of 2',26.22,'2nd Quarter',NULL,'47-42','+1','DEN','MIA',47,42,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('1:59','B. Adebayo makes 2-pt layup from 3 ft (assist by G. Vincent)',25.98,'2nd Quarter','+2','49-42',NULL,'DEN','MIA',49,42,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('1:34','B. Adebayo makes 2-pt jump shot from 3 ft',25.57,'2nd Quarter','+2','51-42',NULL,'DEN','MIA',51,42,-9,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('0:25','M. Porter makes 2-pt dunk from 1 ft (assist by N. Jokić)',24.42,'2nd Quarter',NULL,'51-44','+2','DEN','MIA',51,44,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('12:00','Start of 3rd quarter',24.00,'3rd Quarter','Start of 3rd quarter','Start of 3rd quarter','Start of 3rd quarter','DEN','MIA',51,44,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('0:00','End of 2nd quarter',24.00,'2nd Quarter','End of 2nd quarter','End of 2nd quarter','End of 2nd quarter','DEN','MIA',51,44,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('11:28','N. Jokić makes 2-pt jump shot from 4 ft',23.47,'3rd Quarter',NULL,'51-46','+2','DEN','MIA',51,46,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('11:28','N. Jokić makes free throw 1 of 1',23.47,'3rd Quarter',NULL,'51-47','+1','DEN','MIA',51,47,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('11:17','M. Strus makes 2-pt jump shot from 9 ft (assist by G. Vincent)',23.28,'3rd Quarter','+2','53-47',NULL,'DEN','MIA',53,47,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('10:40','G. Vincent makes 2-pt jump shot from 22 ft',22.67,'3rd Quarter','+2','55-47',NULL,'DEN','MIA',55,47,-8,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('9:17','M. Porter makes 2-pt jump shot from 3 ft',21.28,'3rd Quarter',NULL,'55-49','+2','DEN','MIA',55,49,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('8:45','J. Murray makes 2-pt layup from 3 ft',20.75,'3rd Quarter',NULL,'55-51','+2','DEN','MIA',55,51,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('8:33','K. Love makes 3-pt jump shot from 26 ft (assist by J. Butler)',20.55,'3rd Quarter','+3','58-51',NULL,'DEN','MIA',58,51,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('8:14','N. Jokić makes 2-pt hook shot from 4 ft',20.23,'3rd Quarter',NULL,'58-53','+2','DEN','MIA',58,53,-5,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('8:00','G. Vincent makes 2-pt jump shot from 20 ft',20.00,'3rd Quarter','+2','60-53',NULL,'DEN','MIA',60,53,-7,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('7:45','A. Gordon makes free throw 1 of 2',19.75,'3rd Quarter',NULL,'60-54','+1','DEN','MIA',60,54,-6,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('7:32','N. Jokić makes 2-pt layup at rim',19.53,'3rd Quarter',NULL,'60-56','+2','DEN','MIA',60,56,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('7:02','N. Jokić makes free throw 2 of 2',19.03,'3rd Quarter',NULL,'60-57','+1','DEN','MIA',60,57,-3,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('6:46','J. Murray makes 3-pt jump shot from 23 ft (assist by M. Porter)',18.77,'3rd Quarter',NULL,'60-60','+3','DEN','MIA',60,60,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('5:47','M. Strus makes 2-pt layup from 3 ft (assist by J. Butler)',17.78,'3rd Quarter','+2','62-60',NULL,'DEN','MIA',62,60,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('3:58','C. Martin makes 2-pt layup from 3 ft (assist by K. Lowry)',15.97,'3rd Quarter','+2','64-60',NULL,'DEN','MIA',64,60,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:18','Jump ball: B. Brown vs. G. Vincent (K. Caldwell-Pope gains possession)',15.30,'3rd Quarter','Jump ball: B. Brown vs. G. Vincent (K. Caldwell-Pope gains possession)','Jump ball: B. Brown vs. G. Vincent (K. Caldwell-Pope gains possession)','Jump ball: B. Brown vs. G. Vincent (K. Caldwell-Pope gains possession)','DEN','MIA',64,60,-4,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('2:45','B. Brown makes 2-pt layup at rim',14.75,'3rd Quarter',NULL,'64-62','+2','DEN','MIA',64,62,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('2:25','M. Porter makes 2-pt layup from 2 ft',14.42,'3rd Quarter',NULL,'64-64','+2','DEN','MIA',64,64,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('2:05','G. Vincent makes 2-pt jump shot from 8 ft (assist by D. Robinson)',14.08,'3rd Quarter','+2','66-64',NULL,'DEN','MIA',66,64,-2,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('1:49','C. Braun makes free throw 2 of 2',13.82,'3rd Quarter',NULL,'66-66','+1','DEN','MIA',66,66,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('1:49','C. Braun makes free throw 1 of 2',13.82,'3rd Quarter',NULL,'66-65','+1','DEN','MIA',66,65,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('1:31','M. Porter makes 3-pt jump shot from 25 ft',13.52,'3rd Quarter',NULL,'66-69','+3','DEN','MIA',66,69,3,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('1:10','B. Adebayo makes 2-pt jump shot from 13 ft (assist by D. Robinson)',13.17,'3rd Quarter','+2','68-69',NULL,'DEN','MIA',68,69,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('0:54','N. Jokić makes free throw 2 of 2',12.90,'3rd Quarter',NULL,'68-70','+1','DEN','MIA',68,70,2,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('0:33','K. Lowry makes 3-pt jump shot from 30 ft',12.55,'3rd Quarter','+3','71-70',NULL,'DEN','MIA',71,70,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('12:00','Start of 4th quarter',12.00,'4th Quarter','Start of 4th quarter','Start of 4th quarter','Start of 4th quarter','DEN','MIA',71,70,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('0:00','End of 3rd quarter',12.00,'3rd Quarter','End of 3rd quarter','End of 3rd quarter','End of 3rd quarter','DEN','MIA',71,70,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA'),
	 ('11:39','N. Jokić makes 2-pt hook shot from 3 ft (assist by J. Murray)',11.65,'4th Quarter',NULL,'71-72','+2','DEN','MIA',71,72,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('11:00','J. Murray makes 3-pt jump shot from 25 ft (assist by A. Gordon)',11.00,'4th Quarter',NULL,'71-75','+3','DEN','MIA',71,75,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('10:32','C. Martin makes 2-pt layup from 3 ft (assist by J. Butler)',10.53,'4th Quarter','+2','73-75',NULL,'DEN','MIA',73,75,2,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('10:03','N. Jokić makes 2-pt jump shot from 4 ft (assist by J. Murray)',10.05,'4th Quarter',NULL,'73-77','+2','DEN','MIA',73,77,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('9:38','K. Lowry makes 3-pt jump shot from 23 ft (assist by D. Robinson)',9.63,'4th Quarter','+3','76-77',NULL,'DEN','MIA',76,77,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('9:18','N. Jokić makes 2-pt jump shot from 10 ft (assist by B. Brown)',9.30,'4th Quarter',NULL,'76-79','+2','DEN','MIA',76,79,3,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('6:43','J. Murray makes 2-pt jump shot from 14 ft',6.72,'4th Quarter',NULL,'76-81','+2','DEN','MIA',76,81,5,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('4:43','N. Jokić makes 2-pt jump shot from 6 ft (assist by K. Caldwell-Pope)',4.72,'4th Quarter',NULL,'76-83','+2','DEN','MIA',76,83,7,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('4:29','J. Butler makes 3-pt jump shot from 24 ft (assist by C. Martin)',4.48,'4th Quarter','+3','79-83',NULL,'DEN','MIA',79,83,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('4:06','K. Caldwell-Pope makes 3-pt jump shot from 25 ft (assist by J. Murray)',4.10,'4th Quarter',NULL,'79-86','+3','DEN','MIA',79,86,7,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('3:47','J. Butler makes 3-pt jump shot from 26 ft',3.78,'4th Quarter','+3','82-86',NULL,'DEN','MIA',82,86,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:21','J. Butler makes free throw 3 of 3',3.35,'4th Quarter','+1','85-86',NULL,'DEN','MIA',85,86,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:21','J. Butler makes free throw 2 of 3',3.35,'4th Quarter','+1','84-86',NULL,'DEN','MIA',84,86,2,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('3:21','J. Butler makes free throw 1 of 3',3.35,'4th Quarter','+1','83-86',NULL,'DEN','MIA',83,86,3,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('2:47','J. Butler makes 2-pt jump shot from 10 ft',2.78,'4th Quarter','+2','87-86',NULL,'DEN','MIA',87,86,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('2:24','N. Jokić makes 2-pt layup from 4 ft (assist by J. Murray)',2.40,'4th Quarter',NULL,'87-88','+2','DEN','MIA',87,88,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('1:58','J. Butler makes free throw 1 of 2',1.97,'4th Quarter','+1','88-88',NULL,'DEN','MIA',88,88,0,'2023-06-12','TIE','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA');
INSERT INTO pbp (time_quarter,play,time_remaining_final,quarter,away_score,score,home_score,home_team,away_team,score_away,score_home,margin_score,"date",leading_team,home_team_full,home_primary_color,away_team_full,away_primary_color,game_description,away_fill,home_fill,scoring_team_color,scoring_team,max_home_lead,max_away_lead,winning_team,losing_team) VALUES
	 ('1:58','J. Butler makes free throw 2 of 2',1.97,'4th Quarter','+1','89-88',NULL,'DEN','MIA',89,88,-1,'2023-06-12','MIA','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#98002e','MIA',8,-10,'DEN','MIA'),
	 ('1:31','B. Brown makes 2-pt layup at rim',1.52,'4th Quarter',NULL,'89-90','+2','DEN','MIA',89,90,1,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:24','K. Caldwell-Pope makes free throw 2 of 2',0.40,'4th Quarter',NULL,'89-92','+1','DEN','MIA',89,92,3,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:24','K. Caldwell-Pope makes free throw 1 of 2',0.40,'4th Quarter',NULL,'89-91','+1','DEN','MIA',89,91,2,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:14','B. Brown makes free throw 1 of 2',0.23,'4th Quarter',NULL,'89-93','+1','DEN','MIA',89,93,4,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:14','B. Brown makes free throw 2 of 2',0.23,'4th Quarter',NULL,'89-94','+1','DEN','MIA',89,94,5,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#4d90cd','DEN',8,-10,'DEN','MIA'),
	 ('0:00','End of 4th quarter',0.00,'4th Quarter','End of 4th quarter','End of 4th quarter','End of 4th quarter','DEN','MIA',89,94,5,'2023-06-12','DEN','Denver Nuggets','#4d90cd','Miami Heat','#98002e','Denver Nuggets Vs. Miami Heat','<span style=''color:#98002e'';>Miami Heat</span>','<span style=''color:#4d90cd'';>Denver Nuggets</span>','#808080','TIE',8,-10,'DEN','MIA');

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

INSERT INTO standings ("rank",team,team_full,conference,wins,losses,games_played,win_pct,active_injuries,active_protocols,last_10) VALUES
	 ('1st','MIL','Milwaukee Bucks','Eastern',58,24,82,0.707,0,0,'6-4'),
	 ('2nd','BOS','Boston Celtics','Eastern',57,25,82,0.695,0,0,'8-2'),
	 ('3rd','PHI','Philadelphia 76ers','Eastern',54,28,82,0.659,1,0,'5-5'),
	 ('4th','CLE','Cleveland Cavaliers','Eastern',51,31,82,0.622,1,0,'7-3'),
	 ('5th','NYK','New York Knicks','Eastern',47,35,82,0.573,0,0,'5-5'),
	 ('6th','BKN','Brooklyn Nets','Eastern',45,37,82,0.549,0,0,'6-4'),
	 ('7th','MIA','Miami Heat','Eastern',44,38,82,0.537,0,0,'6-4'),
	 ('8th','ATL','Atlanta Hawks','Eastern',41,41,82,0.500,0,0,'5-5'),
	 ('9th','TOR','Toronto Raptors','Eastern',41,41,82,0.500,0,0,'6-4'),
	 ('10th','CHI','Chicago Bulls','Eastern',40,42,82,0.488,1,0,'6-4');
INSERT INTO standings ("rank",team,team_full,conference,wins,losses,games_played,win_pct,active_injuries,active_protocols,last_10) VALUES
	 ('11th','WAS','Washington Wizards','Eastern',35,47,82,0.427,0,0,'3-7'),
	 ('12th','IND','Indiana Pacers','Eastern',35,47,82,0.427,0,0,'3-7'),
	 ('13th','ORL','Orlando Magic','Eastern',34,48,82,0.415,0,0,'5-5'),
	 ('14th','CHA','Charlotte Hornets','Eastern',27,55,82,0.329,1,0,'5-5'),
	 ('15th','DET','Detroit Pistons','Eastern',17,65,82,0.207,0,0,'1-9'),
	 ('1st','DEN','Denver Nuggets','Western',53,29,82,0.646,1,0,'5-5'),
	 ('2nd','MEM','Memphis Grizzlies','Western',51,31,82,0.622,1,0,'6-4'),
	 ('3rd','SAC','Sacramento Kings','Western',48,34,82,0.585,0,0,'5-5'),
	 ('4th','PHX','Phoenix Suns','Western',45,37,82,0.549,0,0,'7-3'),
	 ('5th','GSW','Golden State Warriors','Western',44,38,82,0.537,0,0,'8-2');
INSERT INTO standings ("rank",team,team_full,conference,wins,losses,games_played,win_pct,active_injuries,active_protocols,last_10) VALUES
	 ('6th','LAC','Los Angeles Clippers','Western',44,38,82,0.537,1,0,'6-4'),
	 ('7th','LAL','Los Angeles Lakers','Western',43,39,82,0.524,0,0,'8-2'),
	 ('8th','MIN','Minnesota Timberwolves','Western',42,40,82,0.512,1,0,'7-3'),
	 ('9th','NOP','New Orleans Pelicans','Western',42,40,82,0.512,1,0,'7-3'),
	 ('10th','OKC','Oklahoma City Thunder','Western',40,42,82,0.488,0,0,'4-6'),
	 ('11th','DAL','Dallas Mavericks','Western',38,44,82,0.463,0,0,'2-8'),
	 ('12th','UTA','Utah Jazz','Western',37,45,82,0.451,0,0,'2-8'),
	 ('13th','POR','Portland Trail Blazers','Western',33,49,82,0.402,0,0,'1-9'),
	 ('14th','SAS','San Antonio Spurs','Western',22,60,82,0.268,1,0,'3-7'),
	 ('15th','HOU','Houston Rockets','Western',22,60,82,0.268,1,0,'4-6');

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

DROP TABLE IF EXISTS reddit_sentiment_time_series;
CREATE TABLE IF NOT EXISTS reddit_sentiment_time_series
(
    team text COLLATE pg_catalog."default",
    scrape_date date,
    potential_game_date date,
    num_comments bigint,
    avg_score numeric,
    avg_neu numeric,
    avg_neg numeric,
    avg_pos numeric,
    avg_compound numeric,
    game_date integer,
    game_outcome text COLLATE pg_catalog."default"
);

INSERT INTO reddit_sentiment_time_series(
	team, scrape_date, potential_game_date, num_comments, avg_score, avg_neu, avg_neg, avg_pos, avg_compound, game_date, game_outcome)
	VALUES ('GSW', current_date, current_date - INTERVAL '1 DAY', 379, 44.826, 0.801, 0.072, 0.127, 0.119, 0, 'NO GAME'),
           ('GSW', current_date - INTERVAL '1 DAY', current_date - INTERVAL '2 DAY', 267, 42.826, 0.783, 0.071, 0.146, 0.161, 0, 'NO GAME'),
           ('GSW', current_date - INTERVAL '2 DAY', current_date - INTERVAL '3 DAY', 611, 33.826, 0.780, 0.070, 0.141, 0.138, 1, 'W'),
           ('GSW', current_date - INTERVAL '3 DAY', current_date - INTERVAL '4 DAY', 162, 31.826, 0.761, 0.088, 0.150, 0.130, 0, 'NO GAME');

DROP TABLE IF EXISTS rolling_avg_stats;
CREATE TABLE IF NOT EXISTS rolling_avg_stats (
	player text NULL,
	rolling_avg_pts numeric NULL,
	rolling_avg_ts_percent numeric NULL,
	rolling_avg_mvp_calc numeric NULL,
	rolling_avg_plusminus numeric NULL,
	team text NULL,
	season_avg_ppg numeric NULL,
	season_ts_percent numeric NULL,
	season_avg_plusminus numeric NULL,
	player_mvp_calc_adj numeric NULL,
	ppg_differential numeric NULL,
	ppg_diff_rank text NULL,
	ts_differential numeric NULL,
	ts_diff_rank text NULL,
	plusminus_differential numeric NULL,
	plusminus_diff_rank text NULL,
	mvp_calc_differential numeric NULL,
	mvp_calc_diff_rank text NULL
);

INSERT INTO nba_prod.rolling_avg_stats (player,rolling_avg_pts,rolling_avg_ts_percent,rolling_avg_mvp_calc,rolling_avg_plusminus,team,season_avg_ppg,season_ts_percent,season_avg_plusminus,player_mvp_calc_adj,ppg_differential,ppg_diff_rank,ts_differential,ts_diff_rank,plusminus_differential,plusminus_diff_rank,mvp_calc_differential,mvp_calc_diff_rank) VALUES
	 ('Tristan Thompson',1.4,0.384,3.4,1.6,NULL,NULL,NULL,NULL,NULL,NULL,'1st',NULL,'3rd',NULL,'1st',NULL,'1st'),
	 ('DaQuan Jeffries',0.0,NULL,-1.5,-3.0,NULL,NULL,NULL,NULL,NULL,NULL,'2nd',NULL,'2nd',NULL,'2nd',NULL,'2nd'),
	 ('Shaedon Sharpe',23.7,0.574,25.7,-10.6,'POR',9.9,0.568,-3.5,11.40,13.8,'3rd',0.006,'199th',-7.1,'523rd',14.30,'7th'),
	 ('Talen Horton-Tucker',20.2,0.488,26.4,-6.3,'UTA',10.7,0.508,-0.1,16.86,9.5,'4th',-0.020,'276th',-6.2,'512nd',9.54,'19th'),
	 ('Svi Mykhailiuk',16.0,0.608,24.6,-0.9,'CHA',6.9,0.584,0.6,7.95,9.1,'5th',0.024,'151st',-1.5,'352nd',16.65,'5th'),
	 ('Kevin Knox',14.5,0.502,12.1,-13.0,'POR',6.6,0.579,-3.5,6.58,7.9,'6th',-0.077,'401st',-9.5,'537th',5.52,'75th'),
	 ('Trey Murphy',22.2,0.728,32.4,5.2,'NOP',14.5,0.650,0.5,20.80,7.7,'7th',0.078,'56th',4.7,'11th',11.60,'13th'),
	 ('Corey Kispert',18.6,0.667,18.3,-5.3,'WAS',11.1,0.656,-1.6,13.40,7.5,'8th',0.011,'182nd',-3.7,'453rd',4.90,'92nd'),
	 ('Johnny Davis',12.6,0.444,19.6,-0.2,'WAS',5.8,0.446,-1.8,6.00,6.8,'9th',-0.002,'226th',1.6,'88th',13.60,'8th'),
	 ('Ochai Agbaji',14.7,0.497,17.1,-5.1,'UTA',7.9,0.561,-0.3,9.03,6.8,'10th',-0.064,'370th',-4.8,'479th',8.07,'35th');

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
	VALUES ('https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629630.png', '<span style=''font-size:16px; color:royalblue;''>Ja Morant</span> <span style=''font-size:12px; color:grey;''>MEM</span>', 'Out - Suspension', 0, 61, 26.2, 41.4, 0.557, 5.0),
           ('https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629645.png', '<span style=''font-size:16px; color:royalblue;''>Kevin Porter</span> <span style=''font-size:12px; color:grey;''>HOU</span>', 'Day To Day - Possible suspension', 1, 59, 19.2, 26.1, 0.565, -5.8);

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

DROP TABLE IF EXISTS social_media_aggs;
CREATE TABLE IF NOT EXISTS social_media_aggs
(
    date date,
    reddit_tot_comments bigint,
    reddit_pct_difference numeric,
    twitter_tot_comments bigint,
    twitter_pct_difference numeric
);

INSERT INTO social_media_aggs(
	date, reddit_tot_comments, reddit_pct_difference, twitter_tot_comments, twitter_pct_difference)
	VALUES (current_date, 4753, -23.600, 0, 0);

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

DROP TABLE IF EXISTS opp_stats;
CREATE TABLE IF NOT EXISTS opp_stats (
	team text NULL,
	scrape_date date NULL,
	fg_percent_opp float8 NULL,
	threep_percent_opp float8 NULL,
	threep_made_opp float8 NULL,
	ppg_opp float8 NULL,
	fg_percent_rank text NULL,
	three_percent_rank text NULL,
	three_pm_rank text NULL,
	ppg_opp_rank text NULL,
	conference text NULL
);

INSERT INTO opp_stats (team,scrape_date,fg_percent_opp,threep_percent_opp,threep_made_opp,ppg_opp,fg_percent_rank,three_percent_rank,three_pm_rank,ppg_opp_rank,conference) VALUES
	 ('Memphis Grizzlies','2023-09-30',0.453,0.355,13.0,113.0,'1st','9th','25th','11th','West'),
	 ('Milwaukee Bucks','2023-09-30',0.456,0.354,12.1,113.3,'2nd','8th','11th','14th','East'),
	 ('New York Knicks','2023-09-30',0.462,0.357,13.0,113.1,'3rd','11th','27th','12th','East'),
	 ('Boston Celtics','2023-09-30',0.463,0.345,11.6,111.4,'4th','4th','5th','4th','East'),
	 ('Brooklyn Nets','2023-09-30',0.463,0.367,11.8,112.5,'5th','22nd','7th','9th','East'),
	 ('Phoenix Suns','2023-09-30',0.466,0.357,11.4,111.6,'6th','12th','3rd','6th','West'),
	 ('Chicago Bulls','2023-09-30',0.468,0.357,13.2,111.8,'7th','14th','29th','7th','East'),
	 ('Cleveland Cavaliers','2023-09-30',0.468,0.368,11.3,106.9,'8th','23rd','2nd','1st','East'),
	 ('Los Angeles Lakers','2023-09-30',0.469,0.344,12.5,116.6,'9th','2nd','18th','20th','West'),
	 ('Golden State Warriors','2023-09-30',0.469,0.364,12.9,117.1,'10th','18th','23rd','21st','West');
INSERT INTO opp_stats (team,scrape_date,fg_percent_opp,threep_percent_opp,threep_made_opp,ppg_opp,fg_percent_rank,three_percent_rank,three_pm_rank,ppg_opp_rank,conference) VALUES
	 ('Minnesota Timberwolves','2023-09-30',0.471,0.369,12.3,115.8,'11th','24th','16th','18th','West'),
	 ('New Orleans Pelicans','2023-09-30',0.472,0.339,12.2,112.5,'12th','1st','15th','10th','West'),
	 ('Philadelphia 76ers','2023-09-30',0.473,0.348,11.6,110.9,'13th','5th','6th','3rd','East'),
	 ('Utah Jazz','2023-09-30',0.473,0.361,12.5,118.0,'14th','17th','19th','24th','West'),
	 ('Washington Wizards','2023-09-30',0.473,0.366,12.0,114.4,'15th','20th','9th','17th','East'),
	 ('Los Angeles Clippers','2023-09-30',0.474,0.365,12.2,113.1,'16th','19th','12th','13th','West'),
	 ('Oklahoma City Thunder','2023-09-30',0.474,0.358,12.9,116.4,'17th','15th','24th','19th','West'),
	 ('Orlando Magic','2023-09-30',0.476,0.351,13.0,114.0,'18th','6th','26th','15th','East'),
	 ('Charlotte Hornets','2023-09-30',0.477,0.357,12.2,117.2,'19th','13th','13th','22nd','East'),
	 ('Denver Nuggets','2023-09-30',0.478,0.344,11.4,112.5,'20th','3rd','4th','8th','West');
INSERT INTO opp_stats (team,scrape_date,fg_percent_opp,threep_percent_opp,threep_made_opp,ppg_opp,fg_percent_rank,three_percent_rank,three_pm_rank,ppg_opp_rank,conference) VALUES
	 ('Houston Rockets','2023-09-30',0.482,0.374,14.5,118.6,'21st','28th','30th','28th','West'),
	 ('Miami Heat','2023-09-30',0.482,0.367,13.1,109.8,'22nd','21st','28th','2nd','East'),
	 ('Dallas Mavericks','2023-09-30',0.485,0.352,11.1,114.1,'23rd','7th','1st','16th','West'),
	 ('Indiana Pacers','2023-09-30',0.485,0.373,12.4,119.5,'24th','26th','17th','29th','East'),
	 ('Atlanta Hawks','2023-09-30',0.486,0.356,11.9,118.1,'25th','10th','8th','26th','East'),
	 ('Detroit Pistons','2023-09-30',0.489,0.36,12.0,118.5,'26th','16th','10th','27th','East'),
	 ('Toronto Raptors','2023-09-30',0.491,0.374,12.2,111.4,'27th','27th','14th','5th','East'),
	 ('Portland Trail Blazers','2023-09-30',0.491,0.379,12.5,117.4,'28th','29th','20th','23rd','West'),
	 ('Sacramento Kings','2023-09-30',0.492,0.373,12.5,118.1,'29th','25th','21st','25th','West'),
	 ('San Antonio Spurs','2023-09-30',0.507,0.391,12.6,123.1,'30th','30th','22nd','30th','West');

DROP TABLE IF EXISTS preseason_odds;
CREATE TABLE IF NOT EXISTS preseason_odds (
	team text NULL,
	team_full text NULL,
	conference text NULL,
	predicted_wins numeric NULL,
	predicted_losses float8 NULL,
	projected_wins numeric NULL,
	projected_losses numeric NULL,
	championship_odds numeric NULL,
	wins_differential numeric NULL,
	predicted_stats text NULL,
	projected_stats text NULL,
	over_under text NULL
);

INSERT INTO preseason_odds (team,team_full,conference,predicted_wins,predicted_losses,projected_wins,projected_losses,championship_odds,wins_differential,predicted_stats,projected_stats,over_under) VALUES
	 ('MIL','Milwaukee Bucks','Eastern',54.5,27.5,58,24,850,3.5,'54.5 - 27.5','58 - 24','Over'),
	 ('BOS','Boston Celtics','Eastern',45.5,36.5,57,25,4000,11.5,'45.5 - 36.5','57 - 25','Over'),
	 ('PHI','Philadelphia 76ers','Eastern',50.5,31.5,54,28,1600,3.5,'50.5 - 31.5','54 - 28','Over'),
	 ('DEN','Denver Nuggets','Western',47.5,34.5,53,29,2200,5.5,'47.5 - 34.5','53 - 29','Over'),
	 ('MEM','Memphis Grizzlies','Western',41.5,40.5,51,31,10000,9.5,'41.5 - 40.5','51 - 31','Over'),
	 ('CLE','Cleveland Cavaliers','Eastern',26.5,55.5,51,31,50000,24.5,'26.5 - 55.5','51 - 31','Over'),
	 ('SAC','Sacramento Kings','Western',36.5,45.5,48,34,25000,11.5,'36.5 - 45.5','48 - 34','Over'),
	 ('NYK','New York Knicks','Eastern',41.5,40.5,47,35,8000,5.5,'41.5 - 40.5','47 - 35','Over'),
	 ('PHX','Phoenix Suns','Western',51.5,30.5,45,37,1400,-6.5,'51.5 - 30.5','45 - 37','Under'),
	 ('BKN','Brooklyn Nets','Eastern',56.5,25.5,45,37,230,-11.5,'56.5 - 25.5','45 - 37','Under');
INSERT INTO preseason_odds (team,team_full,conference,predicted_wins,predicted_losses,projected_wins,projected_losses,championship_odds,wins_differential,predicted_stats,projected_stats,over_under) VALUES
	 ('GSW','Golden State Warriors','Western',48.5,33.5,44,38,1100,-4.5,'48.5 - 33.5','44 - 38','Under'),
	 ('MIA','Miami Heat','Eastern',48.5,33.5,44,38,3500,-4.5,'48.5 - 33.5','44 - 38','Under'),
	 ('LAC','Los Angeles Clippers','Western',45.5,36.5,44,38,1600,-1.5,'45.5 - 36.5','44 - 38','Under'),
	 ('LAL','Los Angeles Lakers','Western',52.5,29.5,43,39,425,-9.5,'52.5 - 29.5','43 - 39','Under'),
	 ('NOP','New Orleans Pelicans','Western',39.5,42.5,42,40,8000,2.5,'39.5 - 42.5','42 - 40','Over'),
	 ('MIN','Minnesota Timberwolves','Western',35.5,46.5,42,40,25000,6.5,'35.5 - 46.5','42 - 40','Over'),
	 ('TOR','Toronto Raptors','Eastern',35.5,46.5,41,41,10000,5.5,'35.5 - 46.5','41 - 41','Over'),
	 ('ATL','Atlanta Hawks','Eastern',47.5,34.5,41,41,3500,-6.5,'47.5 - 34.5','41 - 41','Under'),
	 ('OKC','Oklahoma City Thunder','Western',23.5,58.5,40,42,50000,16.5,'23.5 - 58.5','40 - 42','Over'),
	 ('CHI','Chicago Bulls','Eastern',42.5,39.5,40,42,12500,-2.5,'42.5 - 39.5','40 - 42','Under');
INSERT INTO preseason_odds (team,team_full,conference,predicted_wins,predicted_losses,projected_wins,projected_losses,championship_odds,wins_differential,predicted_stats,projected_stats,over_under) VALUES
	 ('DAL','Dallas Mavericks','Western',48.5,33.5,38,44,2800,-10.5,'48.5 - 33.5','38 - 44','Under'),
	 ('UTA','Utah Jazz','Western',52.5,29.5,37,45,1400,-15.5,'52.5 - 29.5','37 - 45','Under'),
	 ('WAS','Washington Wizards','Eastern',33.5,48.5,35,47,15000,1.5,'33.5 - 48.5','35 - 47','Over'),
	 ('IND','Indiana Pacers','Eastern',42.5,39.5,35,47,10000,-7.5,'42.5 - 39.5','35 - 47','Under'),
	 ('ORL','Orlando Magic','Eastern',22.5,59.5,34,48,50000,11.5,'22.5 - 59.5','34 - 48','Over'),
	 ('POR','Portland Trail Blazers','Western',44.5,37.5,33,49,5000,-11.5,'44.5 - 37.5','33 - 49','Under'),
	 ('CHA','Charlotte Hornets','Eastern',38.5,43.5,27,55,10000,-11.5,'38.5 - 43.5','27 - 55','Under'),
	 ('SAS','San Antonio Spurs','Western',28.5,53.5,22,60,25000,-6.5,'28.5 - 53.5','22 - 60','Under'),
	 ('HOU','Houston Rockets','Western',27.5,54.5,22,60,50000,-5.5,'27.5 - 54.5','22 - 60','Under'),
	 ('DET','Detroit Pistons','Eastern',24.5,57.5,17,65,50000,-7.5,'24.5 - 57.5','17 - 65','Under');

DROP TABLE IF EXISTS recent_games_players;
CREATE TABLE IF NOT EXISTS recent_games_players (
	player text NULL,
	player_new text NULL,
	player_logo text NULL,
	outcome text NULL,
	team text NULL,
	salary numeric NULL,
	pts numeric NULL,
	game_ts_percent numeric NULL,
	pts_color text NULL,
	ts_color text NULL,
	plusminus text NULL
);

INSERT INTO recent_games_players (player,player_new,player_logo,outcome,team,salary,pts,game_ts_percent,pts_color,ts_color,plusminus) VALUES
	 ('Nikola Jokic','<span style=''font-size:16px; color:royalblue;''>Nikola Jokic</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/203999.png','W','DEN',47607350,28,0.769,'0','0','+12'),
	 ('Jimmy Butler','<span style=''font-size:16px; color:royalblue;''>Jimmy Butler</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/202710.png','L','MIA',45183960,21,0.460,'0','0','-3'),
	 ('Bam Adebayo','<span style=''font-size:16px; color:royalblue;''>Bam Adebayo</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1628389.png','L','MIA',32600060,20,0.479,'0','0','-3'),
	 ('Michael Porter','<span style=''font-size:16px; color:royalblue;''>Michael Porter</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629008.png','W','DEN',33386850,16,0.447,'0','0','-7'),
	 ('Jamal Murray','<span style=''font-size:16px; color:royalblue;''>Jamal Murray</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1627750.png','W','DEN',33833400,14,0.467,'0','0','+12'),
	 ('Kyle Lowry','<span style=''font-size:16px; color:royalblue;''>Kyle Lowry</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/200768.png','L','MIA',29682540,12,0.462,'0','0','+5'),
	 ('Max Strus','<span style=''font-size:16px; color:royalblue;''>Max Strus</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629622.png','L','MIA',14487684,12,0.482,'0','0','+2'),
	 ('Kentavious Caldwell-Pope','<span style=''font-size:16px; color:royalblue;''>Kentavious Caldwell-Pope</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/203484.png','W','DEN',14704938,11,0.506,'0','0','+7'),
	 ('Bruce Brown','<span style=''font-size:16px; color:royalblue;''>Bruce Brown</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1628971.png','W','DEN',22000000,10,0.317,'0','0','0'),
	 ('Caleb Martin','<span style=''font-size:16px; color:royalblue;''>Caleb Martin</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1628997.png','L','MIA',6802950,10,0.506,'0','0','+13');
INSERT INTO recent_games_players (player,player_new,player_logo,outcome,team,salary,pts,game_ts_percent,pts_color,ts_color,plusminus) VALUES
	 ('Christian Braun','<span style=''font-size:16px; color:royalblue;''>Christian Braun</span> <span style=''font-size:12px; color:grey;''>DEN</span>',NULL,'W','DEN',2949120,7,0.527,'0','0','0'),
	 ('Gabe Vincent','<span style=''font-size:16px; color:royalblue;''>Gabe Vincent</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629216.png','L','MIA',10500000,6,0.231,'0','0','-14'),
	 ('Duncan Robinson','<span style=''font-size:16px; color:royalblue;''>Duncan Robinson</span> <span style=''font-size:12px; color:grey;''>MIA</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1629130.png','L','MIA',18154000,5,0.417,'0','0','-9'),
	 ('Aaron Gordon','<span style=''font-size:16px; color:royalblue;''>Aaron Gordon</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/203932.png','W','DEN',22266182,4,0.258,'3','0','+8'),
	 ('Jeff Green','<span style=''font-size:16px; color:royalblue;''>Jeff Green</span> <span style=''font-size:12px; color:grey;''>DEN</span>','https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/201145.png','W','DEN',9600000,4,1.000,'0','0','-5');

DROP TABLE IF EXISTS recent_games_teams;
CREATE TABLE IF NOT EXISTS recent_games_teams (
	team text NULL,
	opponent text NULL,
	"date" date NULL,
	outcome text NULL,
	pts_scored numeric NULL,
	pts_scored_opp numeric NULL,
	mov numeric NULL,
	max_team_lead numeric NULL,
	max_opponent_lead numeric NULL,
	team_max_score numeric NULL,
	team_avg_score numeric NULL,
	pts_color text NULL,
	opp_pts_color text NULL,
	team_logo text NULL,
	opp_logo text NULL,
	home_team text NULL,
	new_loc text NULL
);

INSERT INTO recent_games_teams (team,opponent,"date",outcome,pts_scored,pts_scored_opp,mov,max_team_lead,max_opponent_lead,team_max_score,team_avg_score,pts_color,opp_pts_color,team_logo,opp_logo,home_team,new_loc) VALUES
	 ('DEN','MIA','2023-06-12','W',94,89,5,8,10,146,115.8,'3','3','logos/den.png','logos/mia.png','DEN','Vs.');

DROP TABLE IF EXISTS team_adv_stats;
CREATE TABLE IF NOT EXISTS team_adv_stats (
	team text NULL,
	scrape_date date NULL,
	age numeric NULL,
	w int4 NULL,
	l int4 NULL,
	pw int4 NULL,
	pl int4 NULL,
	mov numeric NULL,
	sos numeric NULL,
	srs numeric NULL,
	ortg numeric NULL,
	drtg numeric NULL,
	nrtg numeric NULL,
	pace numeric NULL,
	ftr numeric NULL,
	three_p_rate numeric NULL,
	ts_percent numeric NULL,
	efg_percent numeric NULL,
	tov_percent numeric NULL,
	orb_percent numeric NULL,
	ft_fga numeric NULL,
	efg_percent_opp numeric NULL,
	tov_percent_opp numeric NULL,
	drb_percent_opp numeric NULL,
	ft_fga_opp numeric NULL,
	arena text NULL,
	attendance numeric NULL,
	att_game numeric NULL,
	team_acronym text NULL,
	conference text NULL,
	primary_color text NULL,
	secondary_color text NULL,
	third_color text NULL,
	previous_season_wins int4 NULL,
	previous_season_rank int4 NULL,
	team_logo text NULL
);

INSERT INTO team_adv_stats (team,scrape_date,age,w,l,pw,pl,mov,sos,srs,ortg,drtg,nrtg,pace,ftr,three_p_rate,ts_percent,efg_percent,tov_percent,orb_percent,ft_fga,efg_percent_opp,tov_percent_opp,drb_percent_opp,ft_fga_opp,arena,attendance,att_game,team_acronym,conference,primary_color,secondary_color,third_color,previous_season_wins,previous_season_rank,team_logo) VALUES
	 ('Milwaukee Bucks','2023-06-18',29.8,58,24,50,32,3.63,-0.02,3.61,115.4,111.9,3.5,100.5,0.248,0.446,0.583,0.555,12.7,25,0.184,0.52,10.4,77.8,0.175,'Fiserv Forum',718786,17531,'MIL','Eastern','#00471b','#f0ebd2','NA',51,6,'logos/mil.png'),
	 ('Toronto Raptors','2023-06-18',25.8,41,41,45,37,1.48,0.12,1.59,115.5,114,1.5,97.1,0.257,0.351,0.555,0.517,10.3,27.8,0.201,0.565,15.3,76.7,0.223,'Scotiabank Arena',811261,19787,'TOR','Eastern','#ce1141','#061922','NA',48,10,'logos/tor.png'),
	 ('Boston Celtics','2023-06-18',27.4,57,25,57,25,6.52,-0.15,6.38,118,111.5,6.5,98.5,0.243,0.48,0.6,0.566,12,22.1,0.197,0.528,11.3,78.5,0.18,'TD Garden',766240,18689,'BOS','Eastern','#008348','#061922','#bb9753',51,6,'logos/bos.png'),
	 ('Indiana Pacers','2023-06-18',24.5,35,47,33,49,-3.18,0.28,-2.91,114.6,117.7,-3.1,101.1,0.265,0.413,0.581,0.545,13,23.4,0.209,0.554,13,72.2,0.229,'Gainbridge Fieldhouse',641562,15648,'IND','Eastern','#ffc633','#00275d','#bec0c2',25,26,'logos/ind.png'),
	 ('Miami Heat','2023-06-18',27.7,44,38,40,42,-0.32,0.18,-0.13,113,113.3,-0.3,96.3,0.27,0.408,0.574,0.53,12.4,22.8,0.224,0.561,14.5,77.7,0.198,'Kaseya Center',807190,19688,'MIA','Eastern','#98002e','#f9a01b','NA',53,3,'logos/mia.png'),
	 ('Philadelphia 76ers','2023-06-18',28.2,54,28,52,30,4.32,0.06,4.37,117.7,113.3,4.4,96.9,0.3,0.389,0.608,0.563,12.6,21.6,0.25,0.541,13,77.2,0.217,'Wells Fargo Center',839261,20470,'PHI','Eastern','#ed174c','#006bb6','NA',51,6,'logos/phi.png'),
	 ('Brooklyn Nets','2023-06-18',28,45,37,43,39,0.85,0.18,1.03,115,114.1,0.9,98.3,0.26,0.397,0.598,0.562,12.7,19.6,0.208,0.53,12.2,73.7,0.212,'Barclays Center',724439,17669,'BKN','Eastern','#061922','#061922','#bb9753',44,14,'logos/bkn.png'),
	 ('Orlando Magic','2023-06-18',23.1,34,48,35,47,-2.56,0.17,-2.39,111.6,114.2,-2.6,99.3,0.29,0.361,0.573,0.532,13.4,23.8,0.227,0.55,13.1,77.7,0.211,'Amway Center',728405,17766,'ORL','Eastern','#007dc5','#c4ced3','NA',22,29,'logos/orl.png'),
	 ('Charlotte Hornets','2023-06-18',25.3,27,55,26,56,-6.24,0.35,-5.89,109.2,115.3,-6.1,100.8,0.261,0.36,0.55,0.516,12.3,23.8,0.195,0.544,12.5,75.5,0.211,'Spectrum Center',702052,17123,'CHA','Eastern','#1d1160','#008ca8','#a1a1a4',43,16,'logos/cha.png'),
	 ('Washington Wizards','2023-06-18',26.2,35,47,38,44,-1.21,0.15,-1.06,114.4,115.6,-1.2,98.6,0.258,0.365,0.585,0.55,12.7,22.6,0.202,0.54,11,76.1,0.194,'Capital One Arena',710481,17329,'WAS','Eastern','#002b5c','#e31837','NA',35,21,'logos/was.png');
INSERT INTO team_adv_stats (team,scrape_date,age,w,l,pw,pl,mov,sos,srs,ortg,drtg,nrtg,pace,ftr,three_p_rate,ts_percent,efg_percent,tov_percent,orb_percent,ft_fga,efg_percent_opp,tov_percent_opp,drb_percent_opp,ft_fga_opp,arena,attendance,att_game,team_acronym,conference,primary_color,secondary_color,third_color,previous_season_wins,previous_season_rank,team_logo) VALUES
	 ('Chicago Bulls','2023-06-18',27.5,40,42,44,38,1.29,0.07,1.37,113.5,112.2,1.3,98.5,0.251,0.333,0.587,0.55,12.2,20.1,0.203,0.544,13.5,77.8,0.197,'United Center',841632,20528,'CHI','Eastern','#ce1141','#061922','NA',46,12,'logos/chi.png'),
	 ('New York Knicks','2023-06-18',24.5,47,35,48,34,2.93,0.06,2.99,117.8,114.8,3,97.1,0.285,0.4,0.577,0.541,11.4,28.3,0.217,0.536,11.4,77.1,0.21,'Madison Square Garden (IV)',795110,19393,'NYK','Eastern','#006bb6','#f58426','NA',37,19,'logos/nyk.png'),
	 ('Detroit Pistons','2023-06-18',24.1,17,65,22,60,-8.22,0.49,-7.73,110.7,118.9,-8.2,99,0.295,0.372,0.561,0.52,13.3,24.9,0.227,0.557,11.9,74,0.231,'Little Caesars Arena',759715,18596,'DET','Eastern','#006bb6','#ed174c','#0f586c',23,28,'logos/det.png'),
	 ('Atlanta Hawks','2023-06-18',24.9,41,41,42,40,0.29,0.02,0.32,116.6,116.3,0.3,100.7,0.244,0.331,0.579,0.541,11.2,25.1,0.2,0.552,12.4,75.8,0.206,'State Farm Arena',719787,17556,'ATL','Eastern','#e13a3e','#c4d600','#061922',43,16,'logos/atl.png'),
	 ('Cleveland Cavaliers','2023-06-18',25.4,51,31,55,27,5.38,-0.15,5.23,116.1,110.6,5.5,95.7,0.264,0.371,0.59,0.556,12.3,23.6,0.206,0.535,14.4,76.3,0.21,'Rocket Mortgage Fieldhouse',777280,18958,'CLE','Eastern','#860038','#fdbb30','#002d62',44,14,'logos/cle.png'),
	 ('Los Angeles Lakers','2023-06-18',27.9,43,39,42,40,0.57,-0.15,0.43,114.5,113.9,0.6,101.3,0.299,0.351,0.582,0.542,12.3,22.8,0.232,0.535,10.9,76.3,0.171,'Crypto.com Arena',763168,18614,'LAL','Western','#fdb927','#552582','NA',33,23,'logos/lal.png'),
	 ('Los Angeles Clippers','2023-06-18',29.7,44,38,42,40,0.5,-0.19,0.31,115,114.5,0.5,98,0.278,0.387,0.588,0.551,12.8,22.9,0.217,0.543,11.7,76.6,0.195,'Crypto.com Arena',720543,17574,'LAC','Western','#ed174c','#006bb6','NA',42,18,'logos/lac.png'),
	 ('Denver Nuggets','2023-06-18',26.6,53,29,49,33,3.33,-0.29,3.04,117.6,114.2,3.4,98.1,0.259,0.361,0.601,0.573,13.1,24.8,0.194,0.543,12.2,76.4,0.201,'Ball Arena',788635,19235,'DEN','Western','#4d90cd','#fdb927','NA',48,10,'logos/den.png'),
	 ('Houston Rockets','2023-06-18',22.1,22,60,23,59,-7.85,0.24,-7.62,111.4,119.3,-7.9,99,0.285,0.359,0.554,0.516,14,30.2,0.215,0.564,11.8,75.8,0.218,'Toyota Center',668865,16314,'HOU','Western','#ce1141','#c4ced3','#061922',20,30,'logos/hou.png'),
	 ('Oklahoma City Thunder','2023-06-18',22.8,40,42,44,38,1.09,-0.12,0.96,115.2,114.2,1,101.1,0.256,0.369,0.57,0.531,11.2,24.7,0.207,0.547,14.4,72.9,0.222,'Paycom Center',636903,15534,'OKC','Western','#007dc3','#F05133','NA',24,27,'logos/okc.png');
INSERT INTO team_adv_stats (team,scrape_date,age,w,l,pw,pl,mov,sos,srs,ortg,drtg,nrtg,pace,ftr,three_p_rate,ts_percent,efg_percent,tov_percent,orb_percent,ft_fga,efg_percent_opp,tov_percent_opp,drb_percent_opp,ft_fga_opp,arena,attendance,att_game,team_acronym,conference,primary_color,secondary_color,third_color,previous_season_wins,previous_season_rank,team_logo) VALUES
	 ('Utah Jazz','2023-06-18',26.5,37,45,39,43,-0.94,-0.09,-1.03,115.8,116.7,-0.9,100.5,0.265,0.421,0.584,0.547,13.3,26.8,0.209,0.541,10.9,75.2,0.205,'Vivint Arena',728240,17762,'UTA','Western','#002b5c','#f9a01b','NA',49,9,'logos/uta.png'),
	 ('Dallas Mavericks','2023-06-18',27.8,38,44,41,41,0.07,-0.22,-0.14,116.8,116.7,0.1,96.6,0.298,0.487,0.599,0.565,11.4,18,0.225,0.549,11.9,75.5,0.226,'American Airlines Center',827282,20178,'DAL','Western','#0064b1','#c4ced3','#061922',52,5,'logos/dal.png'),
	 ('Portland Trail Blazers','2023-06-18',25.1,33,49,31,51,-4.01,0.05,-3.96,114.8,118.8,-4,98.6,0.289,0.413,0.589,0.549,13.1,22.4,0.23,0.563,12.1,74.9,0.217,'Moda Center',767374,18716,'POR','Western','#061922','#e03a3e','NA',27,25,'logos/por.png'),
	 ('Memphis Grizzlies','2023-06-18',24.4,51,31,51,31,3.94,-0.34,3.6,115.1,111.2,3.9,101.1,0.259,0.372,0.57,0.54,11.7,26.5,0.19,0.526,13.1,75.9,0.206,'FedEx Forum',707836,17264,'MEM','Western','#7399c6','#bed4e9','#fdb927',56,2,'logos/mem.png'),
	 ('Phoenix Suns','2023-06-18',28.1,45,37,46,36,2.07,0.01,2.08,115.1,113,2.1,98.2,0.241,0.362,0.57,0.535,12,26.6,0.191,0.532,12.9,76,0.234,'Footprint Center',699911,17071,'PHX','Western','#e56020','#1d1160','NA',64,1,'logos/phx.png'),
	 ('San Antonio Spurs','2023-06-18',23.9,22,60,19,63,-10.04,0.22,-9.82,110.2,120,-9.8,101.6,0.229,0.348,0.554,0.525,13,25.6,0.17,0.576,12,74.9,0.201,'AT&T Center',694434,15508,'SAS','Western','#061922','#bac3c9','NA',34,22,'logos/sas.png'),
	 ('Sacramento Kings','2023-06-18',25.4,48,34,47,35,2.65,-0.35,2.3,119.4,116.8,2.6,100.3,0.284,0.423,0.608,0.572,12,22.7,0.225,0.563,12.6,77.2,0.203,'Golden 1 Center',715491,17451,'SAC','Western','#724c9f','#8e9090','NA',30,24,'logos/sac.png'),
	 ('New Orleans Pelicans','2023-06-18',25.9,42,40,46,36,1.89,-0.26,1.63,114.4,112.5,1.9,99.1,0.279,0.344,0.582,0.543,12.9,24.7,0.221,0.543,13.4,77.4,0.212,'Smoothie King Center',687691,16773,'NOP','Western','#002b5c','#e31837','NA',36,20,'logos/nop.png'),
	 ('Minnesota Timberwolves','2023-06-18',25.8,42,40,41,41,-0.04,-0.18,-0.22,113.7,113.8,-0.1,101,0.271,0.381,0.592,0.56,13.6,21.5,0.205,0.54,13.3,74.3,0.225,'Target Center',687510,16769,'MIN','Western','#005083','#00a94f','NA',46,12,'logos/min.png'),
	 ('Golden State Warriors','2023-06-18',27.3,44,38,45,37,1.8,-0.15,1.66,116.1,114.4,1.7,101.6,0.224,0.479,0.6,0.571,14.1,24.4,0.178,0.54,12.3,76,0.214,'Chase Center',740624,18064,'GSW','Western','#fdb927','#006bb6','NA',53,3,'logos/gsw.png');

DROP TABLE IF EXISTS team_blown_leads;
CREATE TABLE IF NOT EXISTS team_blown_leads (
	team text NULL,
	season_type text NULL,
	blown_leads_10pt int8 NULL,
	blown_lead_rank text NULL,
	team_comebacks_10pt int8 NULL,
	comeback_rank text NULL,
	net_comebacks int8 NULL,
	net_rank text NULL
);

INSERT INTO team_blown_leads (team,season_type,blown_leads_10pt,blown_lead_rank,team_comebacks_10pt,comeback_rank,net_comebacks,net_rank) VALUES
	 ('MIA','Playoffs',2,'5th',7,'1st',5,'1st'),
	 ('PHX','Playoffs',0,'30th',3,'4th',3,'2nd'),
	 ('PHI','Playoffs',0,'30th',3,'3rd',3,'3rd'),
	 ('DEN','Playoffs',1,'8th',3,'2nd',2,'4th'),
	 ('LAL','Playoffs',1,'11th',2,'5th',1,'5th'),
	 ('CLE','Playoffs',0,'30th',0,'30th',0,'6th'),
	 ('MEM','Playoffs',0,'30th',0,'30th',0,'7th'),
	 ('ATL','Playoffs',1,'9th',1,'6th',0,'8th'),
	 ('SAC','Playoffs',1,'10th',1,'10th',0,'9th'),
	 ('MIN','Playoffs',1,'12th',0,'30th',-1,'10th');
INSERT INTO team_blown_leads (team,season_type,blown_leads_10pt,blown_lead_rank,team_comebacks_10pt,comeback_rank,net_comebacks,net_rank) VALUES
	 ('NYK','Playoffs',2,'4th',1,'9th',-1,'11th'),
	 ('MIL','Playoffs',2,'7th',0,'30th',-2,'12th'),
	 ('BKN','Playoffs',2,'6th',0,'30th',-2,'13th'),
	 ('GSW','Playoffs',3,'2nd',1,'8th',-2,'14th'),
	 ('LAC','Playoffs',3,'3rd',0,'30th',-3,'15th'),
	 ('BOS','Playoffs',4,'1st',1,'7th',-3,'16th'),
	 ('OKC','Regular Season',7,'30th',17,'1st',10,'1st'),
	 ('PHI','Regular Season',9,'25th',16,'5th',7,'2nd'),
	 ('SAC','Regular Season',8,'28th',15,'8th',7,'3rd'),
	 ('BKN','Regular Season',11,'13th',17,'3rd',6,'4th');
INSERT INTO team_blown_leads (team,season_type,blown_leads_10pt,blown_lead_rank,team_comebacks_10pt,comeback_rank,net_comebacks,net_rank) VALUES
	 ('IND','Regular Season',11,'21st',17,'4th',6,'5th'),
	 ('CLE','Regular Season',12,'9th',17,'2nd',5,'6th'),
	 ('MIL','Regular Season',8,'29th',13,'13th',5,'7th'),
	 ('LAL','Regular Season',9,'23rd',13,'11th',4,'8th'),
	 ('DEN','Regular Season',13,'8th',16,'6th',3,'9th'),
	 ('LAC','Regular Season',12,'11th',15,'7th',3,'10th'),
	 ('MIA','Regular Season',11,'16th',14,'10th',3,'11th'),
	 ('GSW','Regular Season',11,'15th',13,'12th',2,'12th'),
	 ('ORL','Regular Season',11,'18th',11,'18th',0,'13th'),
	 ('DET','Regular Season',8,'27th',8,'23rd',0,'14th');
INSERT INTO team_blown_leads (team,season_type,blown_leads_10pt,blown_lead_rank,team_comebacks_10pt,comeback_rank,net_comebacks,net_rank) VALUES
	 ('MEM','Regular Season',10,'22nd',10,'21st',0,'15th'),
	 ('UTA','Regular Season',9,'24th',9,'22nd',0,'16th'),
	 ('NYK','Regular Season',11,'17th',11,'15th',0,'17th'),
	 ('CHA','Regular Season',11,'20th',11,'16th',0,'18th'),
	 ('CHI','Regular Season',14,'6th',12,'14th',-2,'19th'),
	 ('TOR','Regular Season',12,'12th',8,'26th',-4,'20th'),
	 ('NOP','Regular Season',14,'7th',10,'19th',-4,'21st'),
	 ('HOU','Regular Season',11,'14th',7,'28th',-4,'22nd'),
	 ('POR','Regular Season',19,'1st',15,'9th',-4,'23rd'),
	 ('BOS','Regular Season',12,'10th',8,'24th',-4,'24th');
INSERT INTO team_blown_leads (team,season_type,blown_leads_10pt,blown_lead_rank,team_comebacks_10pt,comeback_rank,net_comebacks,net_rank) VALUES
	 ('SAS','Regular Season',9,'26th',4,'29th',-5,'25th'),
	 ('DAL','Regular Season',15,'5th',10,'20th',-5,'26th'),
	 ('ATL','Regular Season',15,'4th',8,'25th',-7,'27th'),
	 ('MIN','Regular Season',18,'2nd',11,'17th',-7,'28th'),
	 ('PHX','Regular Season',11,'19th',4,'30th',-7,'29th'),
	 ('WAS','Regular Season',15,'3rd',7,'27th',-8,'30th');

DROP TABLE IF EXISTS team_contracts_analysis;
CREATE TABLE IF NOT EXISTS team_contracts_analysis (
	team text NULL,
	win_percentage numeric NULL,
	sum_salary_earned numeric NULL,
	sum_salary_earned_max numeric NULL,
	team_pct_salary_earned numeric NULL,
	record text NULL
);

INSERT INTO team_contracts_analysis (team,win_percentage,sum_salary_earned,sum_salary_earned_max,team_pct_salary_earned,record) VALUES
	 ('PHI',0.659,12946100046,16398920388,0.789,'54 - 28'),
	 ('DEN',0.646,13717005100,16936420056,0.810,'53 - 29'),
	 ('CHI',0.488,10217270968,11323345150,0.902,'40 - 42'),
	 ('DET',0.207,4819130794,7760974460,0.621,'17 - 65'),
	 ('MEM',0.622,9919816478,13295218502,0.746,'51 - 31'),
	 ('MIA',0.537,12780871393,17102948608,0.747,'44 - 38'),
	 ('NYK',0.573,10168829872,12752826714,0.797,'47 - 35'),
	 ('MIN',0.512,9157038732,12845087784,0.713,'42 - 40'),
	 ('DAL',0.463,9174517716,12484684828,0.735,'38 - 44'),
	 ('SAS',0.268,5314811864,7586264932,0.701,'22 - 60');
INSERT INTO team_contracts_analysis (team,win_percentage,sum_salary_earned,sum_salary_earned_max,team_pct_salary_earned,record) VALUES
	 ('ATL',0.500,11595214515,13852182920,0.837,'41 - 41'),
	 ('NOP',0.512,9412946869,14195509622,0.663,'42 - 40'),
	 ('LAL',0.524,9816844956,13296545672,0.738,'43 - 39'),
	 ('BKN',0.549,10818189483,14474249844,0.747,'45 - 37'),
	 ('BOS',0.695,11456714545,13938046678,0.822,'57 - 25'),
	 ('POR',0.402,9126437807,12394179296,0.736,'33 - 49'),
	 ('LAC',0.537,11763775814,16232238496,0.725,'44 - 38'),
	 ('ORL',0.415,5492586761,8996355710,0.611,'34 - 48'),
	 ('WAS',0.427,9457703118,13221773644,0.715,'35 - 47'),
	 ('SAC',0.585,10562539867,11935223082,0.885,'48 - 34');
INSERT INTO team_contracts_analysis (team,win_percentage,sum_salary_earned,sum_salary_earned_max,team_pct_salary_earned,record) VALUES
	 ('CLE',0.622,9560480874,11754481552,0.813,'51 - 31'),
	 ('UTA',0.451,6099900573,8609745554,0.708,'37 - 45'),
	 ('MIL',0.707,11650924225,15795128886,0.738,'58 - 24'),
	 ('OKC',0.488,5711091230,7276504602,0.785,'40 - 42'),
	 ('HOU',0.268,3763667962,4753225202,0.792,'22 - 60'),
	 ('PHX',0.549,10206452528,15046596232,0.678,'45 - 37'),
	 ('TOR',0.500,12174866405,15617561986,0.780,'41 - 41'),
	 ('GSW',0.537,13114560933,17448380414,0.752,'44 - 38'),
	 ('IND',0.427,6045280829,7837835356,0.771,'35 - 47'),
	 ('CHA',0.329,4585776355,7811946644,0.587,'27 - 55');

DROP TABLE IF EXISTS team_game_types;
CREATE TABLE IF NOT EXISTS team_game_types (
	team text NULL,
	outcome_wins_count int8 NULL,
	outcome_losses_count int8 NULL,
	clutch_wins_count int8 NULL,
	clutch_losses_count int8 NULL,
	blowout_wins_count int8 NULL,
	blowout_losses_count int8 NULL,
	tenpt_wins_count int8 NULL,
	tenpt_losses_count int8 NULL
);

INSERT INTO team_game_types (team,outcome_wins_count,outcome_losses_count,clutch_wins_count,clutch_losses_count,blowout_wins_count,blowout_losses_count,tenpt_wins_count,tenpt_losses_count) VALUES
	 ('NOP',42,40,8,11,7,5,10,12),
	 ('MEM',51,31,11,8,12,3,12,9),
	 ('TOR',41,41,8,16,3,2,14,10),
	 ('LAC',44,38,8,11,5,7,17,10),
	 ('SAS',22,60,6,6,1,18,10,16),
	 ('MIN',42,40,14,11,4,5,16,13),
	 ('PHI',54,28,16,8,8,2,14,12),
	 ('CLE',51,31,8,12,12,0,14,8),
	 ('MIL',58,24,9,4,7,7,21,5),
	 ('DEN',53,29,17,8,8,6,9,6);
INSERT INTO team_game_types (team,outcome_wins_count,outcome_losses_count,clutch_wins_count,clutch_losses_count,blowout_wins_count,blowout_losses_count,tenpt_wins_count,tenpt_losses_count) VALUES
	 ('UTA',37,45,13,15,4,5,11,17),
	 ('ATL',41,41,13,12,4,6,11,14),
	 ('DAL',38,44,18,17,6,3,10,16),
	 ('BKN',45,37,14,11,6,6,10,11),
	 ('POR',33,49,10,10,3,8,8,12),
	 ('CHI',40,42,7,14,8,6,11,9),
	 ('WAS',35,47,10,9,5,3,9,23),
	 ('HOU',22,60,9,8,2,10,7,18),
	 ('ORL',34,48,9,13,1,5,11,13),
	 ('CHA',27,55,8,9,2,7,13,14);
INSERT INTO team_game_types (team,outcome_wins_count,outcome_losses_count,clutch_wins_count,clutch_losses_count,blowout_wins_count,blowout_losses_count,tenpt_wins_count,tenpt_losses_count) VALUES
	 ('NYK',47,35,14,10,9,3,11,14),
	 ('OKC',40,42,9,16,4,4,13,14),
	 ('IND',35,47,14,12,1,4,14,12),
	 ('MIA',44,38,24,15,3,5,10,11),
	 ('BOS',57,25,13,11,12,1,14,4),
	 ('DET',17,65,3,12,0,15,8,18),
	 ('PHX',45,37,11,14,8,6,9,6),
	 ('SAC',48,34,15,12,8,3,15,10),
	 ('GSW',44,38,9,11,7,5,12,12),
	 ('LAL',43,39,11,13,2,2,14,9);

DROP TABLE IF EXISTS team_ratings;
CREATE TABLE IF NOT EXISTS team_ratings(
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

INSERT INTO team_ratings (team,team_acronym,w,l,ortg,drtg,nrtg,team_logo,nrtg_rank,drtg_rank,ortg_rank) VALUES
	 ('Boston Celtics','BOS',57,25,118,111.5,6.5,'logos/bos.png','1st','3rd','2nd'),
	 ('Cleveland Cavaliers','CLE',51,31,116.1,110.6,5.5,'logos/cle.png','2nd','1st','8th'),
	 ('Philadelphia 76ers','PHI',54,28,117.7,113.3,4.4,'logos/phi.png','3rd','8th','4th'),
	 ('Memphis Grizzlies','MEM',51,31,115.1,111.2,3.9,'logos/mem.png','4th','2nd','15th'),
	 ('Milwaukee Bucks','MIL',58,24,115.4,111.9,3.5,'logos/mil.png','5th','4th','12th'),
	 ('Denver Nuggets','DEN',53,29,117.6,114.2,3.4,'logos/den.png','6th','14th','5th'),
	 ('New York Knicks','NYK',47,35,117.8,114.8,3,'logos/nyk.png','7th','19th','3rd'),
	 ('Sacramento Kings','SAC',48,34,119.4,116.8,2.6,'logos/sac.png','8th','25th','1st'),
	 ('Phoenix Suns','PHX',45,37,115.1,113,2.1,'logos/phx.png','9th','7th','14th'),
	 ('New Orleans Pelicans','NOP',42,40,114.4,112.5,1.9,'logos/nop.png','10th','6th','22nd');
INSERT INTO team_ratings (team,team_acronym,w,l,ortg,drtg,nrtg,team_logo,nrtg_rank,drtg_rank,ortg_rank) VALUES
	 ('Golden State Warriors','GSW',44,38,116.1,114.4,1.7,'logos/gsw.png','11th','17th','9th'),
	 ('Toronto Raptors','TOR',41,41,115.5,114,1.5,'logos/tor.png','12th','12th','11th'),
	 ('Chicago Bulls','CHI',40,42,113.5,112.2,1.3,'logos/chi.png','13th','5th','24th'),
	 ('Oklahoma City Thunder','OKC',40,42,115.2,114.2,1,'logos/okc.png','14th','16th','13th'),
	 ('Brooklyn Nets','BKN',45,37,115,114.1,0.9,'logos/bkn.png','15th','13th','17th'),
	 ('Los Angeles Lakers','LAL',43,39,114.5,113.9,0.6,'logos/lal.png','16th','11th','20th'),
	 ('Los Angeles Clippers','LAC',44,38,115,114.5,0.5,'logos/lac.png','17th','18th','16th'),
	 ('Atlanta Hawks','ATL',41,41,116.6,116.3,0.3,'logos/atl.png','18th','22nd','7th'),
	 ('Dallas Mavericks','DAL',38,44,116.8,116.7,0.1,'logos/dal.png','19th','23rd','6th'),
	 ('Minnesota Timberwolves','MIN',42,40,113.7,113.8,-0.1,'logos/min.png','20th','10th','23rd');
INSERT INTO team_ratings (team,team_acronym,w,l,ortg,drtg,nrtg,team_logo,nrtg_rank,drtg_rank,ortg_rank) VALUES
	 ('Miami Heat','MIA',44,38,113,113.3,-0.3,'logos/mia.png','21st','9th','25th'),
	 ('Utah Jazz','UTA',37,45,115.8,116.7,-0.9,'logos/uta.png','22nd','24th','10th'),
	 ('Washington Wizards','WAS',35,47,114.4,115.6,-1.2,'logos/was.png','23rd','21st','21st'),
	 ('Orlando Magic','ORL',34,48,111.6,114.2,-2.6,'logos/orl.png','24th','15th','26th'),
	 ('Indiana Pacers','IND',35,47,114.6,117.7,-3.1,'logos/ind.png','25th','26th','19th'),
	 ('Portland Trail Blazers','POR',33,49,114.8,118.8,-4,'logos/por.png','26th','27th','18th'),
	 ('Charlotte Hornets','CHA',27,55,109.2,115.3,-6.1,'logos/cha.png','27th','20th','30th'),
	 ('Houston Rockets','HOU',22,60,111.4,119.3,-7.9,'logos/hou.png','28th','29th','27th'),
	 ('Detroit Pistons','DET',17,65,110.7,118.9,-8.2,'logos/det.png','29th','28th','28th'),
	 ('San Antonio Spurs','SAS',22,60,110.2,120,-9.8,'logos/sas.png','30th','30th','29th');

DROP TABLE IF EXISTS ml_models.tonights_games_ml;
CREATE TABLE IF NOT EXISTS ml_models.tonights_games_ml
(
    index bigint,
    home_team text COLLATE pg_catalog."default",
    home_moneyline double precision,
    away_team text COLLATE pg_catalog."default",
    away_moneyline double precision,
    proper_date date,
    home_team_rank bigint,
    home_days_rest bigint,
    home_team_avg_pts_scored double precision,
    home_team_avg_pts_scored_opp double precision,
    home_team_win_pct double precision,
    home_team_win_pct_last10 double precision,
    home_is_top_players bigint,
    away_team_rank bigint,
    away_days_rest bigint,
    away_team_avg_pts_scored double precision,
    away_team_avg_pts_scored_opp double precision,
    away_team_win_pct double precision,
    away_team_win_pct_last10 double precision,
    away_is_top_players bigint,
    home_team_predicted_win_pct double precision,
    away_team_predicted_win_pct double precision
);

INSERT INTO ml_models.tonights_games_ml(
	index, home_team, home_moneyline, away_team, away_moneyline, proper_date, home_team_rank, home_days_rest, home_team_avg_pts_scored, home_team_avg_pts_scored_opp, home_team_win_pct, home_team_win_pct_last10, home_is_top_players, away_team_rank, away_days_rest, away_team_avg_pts_scored, away_team_avg_pts_scored_opp, away_team_win_pct, away_team_win_pct_last10, away_is_top_players, home_team_predicted_win_pct, away_team_predicted_win_pct)
	VALUES (1, 'Golden State Warriors', '-195', 'Denver Nuggets', 165, current_date, 1, 2, 123, 109, 0.752, 0.655, 2, 18, 1, 102, 123, 0.565, 0.612, 2, 0.828, 0.172);