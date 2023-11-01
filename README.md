# NBA ELT Dashboard
![Tests](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/test.yml/badge.svg) ![Deployment](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/deploy.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/jyablonski/nba_elt_dashboard/badge.svg?branch=master)](https://coveralls.io/github/jyablonski/nba_elt_dashboard?branch=master) ![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

Version: 1.0.1

## [Dashboard](https://nbadashboard.jyablonski.dev)

The NBA Dashboard has the following functionalities:
- Overview of Standings, Contract Value, and Top Player Analysis
- Recent Games Analysis
- NBA Win Prediction Percentages & other Schedule Metrics for upcoming games
- Social Media Analysis

## Running the App
Clone the Repo & run `make up` which spins up the App locally served [here](http://localhost:9090/) using 2 Docker Containers:
- Postgres Database
- Dash Server

When finished run `make down`.

## Tests
To run tests locally, run `make test`.

The same test suite runs on every commit to any PR

## Project
![NBA ELT Pipeline Data Flow 2](https://github.com/jyablonski/nba_elt_rest_api/assets/16946556/67fd15c7-7fed-43cc-a3b8-0e267ca968b3)

1. Links to other Repos providing infrastructure for this Project
    * [Shiny Server](https://github.com/jyablonski/NBA-Dashboard)
    * [Ingestion Script](https://github.com/jyablonski/python_docker)
    * [dbt](https://github.com/jyablonski/nba_elt_dbt)
    * [Terraform](https://github.com/jyablonski/aws_terraform)
    * [Airflow Proof of Concept](https://github.com/jyablonski/nba_elt_airflow)
    * [ML Pipeline](https://github.com/jyablonski/nba_elt_mlflow)