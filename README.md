# NBA Dashboard

![CI/CD](https://github.com/jyablonski/nba_elt_dashboard/actions/workflows/ci_cd.yaml/badge.svg)

The NBA Dashboard is a Python app built with [Dash](https://dash.plotly.com/) that provides the following functionality:

- Overview of standings, contract value, and top-player analysis
- Recent games analysis
- NBA win prediction percentages and other schedule metrics for upcoming games
- Social media analysis

The app is hosted on cloud infrastructure at https://nbadashboard.jyablonski.dev.

## Running the App

Clone the repository and run `make up` to start the app locally at [http://localhost:9000/](http://localhost:9000/). This starts two Docker containers:

- PostgreSQL database
- Dash server

When you are finished, run `make down`.

Run `make test` to run the full test suite.

## Project

For more information, see the [dashboard documentation](https://doqs.jyablonski.dev/services/dash_frontend/).

1. Links to other repositories that support this project
   - [Ingestion Script](https://github.com/jyablonski/nba_elt_ingestion)
   - [dbt](https://github.com/jyablonski/nba_elt_dbt)
   - [ML Pipeline](https://github.com/jyablonski/nba_elt_mlflow)
   - [Terraform](https://github.com/jyablonski/aws_terraform)
   - [REST API](https://github.com/jyablonski/nba_elt_rest_api)
   - [Internal Documentation](https://doqs.jyablonski.dev)
