# NBA ELT Dashboard
![Tests](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/test.yml/badge.svg) ![Deployment](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/deploy.yml/badge.svg) ![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

Version: 1.0.7

## [Dashboard](https://nbadashboard.jyablonski.dev)

The NBA Dashboard has the following functionalities:
- Overview of Standings, Contract Value, and Top Player Analysis
- Recent Games Analysis
- NBA Win Prediction Percentages & other Schedule Metrics for upcoming games
- Social Media Analysis

## Running the App
Clone the Repo & run `make up` which spins up the App locally served [here](http://localhost:9000/) using 2 Docker Containers:
- Postgres Database
- Dash Server

When finished run `make down`.

## Tests
To run tests locally, run `make test`.

The same test suite runs on every commit to any PR

## Project
![nba_pipeline_diagram](https://github.com/jyablonski/nba_elt_dashboard/assets/16946556/e41ee516-9f38-4b4a-bbeb-8447ce35d480)

1. Links to other Repos providing infrastructure for this Project
    * [Ingestion Script](https://github.com/jyablonski/python_docker)
    * [dbt](https://github.com/jyablonski/nba_elt_dbt)
    * [ML Pipeline](https://github.com/jyablonski/nba_elt_mlflow)
    * [Terraform](https://github.com/jyablonski/aws_terraform)
    * [REST API](https://github.com/jyablonski/nba_elt_rest_api)