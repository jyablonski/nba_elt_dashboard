from dash import html

about_layout = html.Div(
    [
        html.Link(
            rel="stylesheet",
            href="../assets/styles.css",
        ),
        html.H1("About this Project"),
        html.P(
            "This dashboard shows up to date information about the 2023-24 NBA Season."
        ),
        html.H3("Data"),
        html.Ul(
            [
                html.Li(
                    [
                        "All NBA Game log, schedule, and play-by-play data \
                        is webscraped daily from ",
                        html.A(
                            "basketball-reference",
                            href="https://www.basketball-reference.com/",
                        ),
                    ]
                ),
                html.Li(
                    [
                        "Reddit Comments are scraped directly from the Top Posts on ",
                        html.A("r/nba", href="https://www.reddit.com/r/nba/"),
                        " via their API",
                    ]
                ),
                html.Li(
                    [
                        "Moneyline Odds are pulled from ",
                        html.A("DraftKings", href="https://www.draftkings.com/"),
                    ]
                ),
                html.Li(
                    "A Logistic Regression ML Model is used to provide Win % Predictions \
                    in the Schedule Tab"
                ),
            ]
        ),
        html.H3("Project Infrastructure"),
        html.P("GitHub Links to Infrastructure for this Project: "),
        html.Ul(
            [
                html.Li(
                    html.A(
                        "Dashboard",
                        href="https://github.com/jyablonski/nba_elt_dashboard",
                    )
                ),
                html.Li(
                    html.A(
                        "Ingestion Script",
                        href="https://github.com/jyablonski/python_docker",
                    )
                ),
                html.Li(
                    html.A(
                        "dbt Transformations",
                        href="https://github.com/jyablonski/nba_elt_dbt",
                    ),
                ),
                html.Li(
                    html.A(
                        "ML Pipeline",
                        href="https://github.com/jyablonski/nba_elt_mlflow",
                    ),
                ),
                html.Li(
                    html.A(
                        "REST API",
                        href="https://github.com/jyablonski/nba_elt_rest_api",
                    ),
                ),
                html.Li(
                    html.A(
                        "Airflow Proof of Concept",
                        href="https://github.com/jyablonski/nba_elt_airflow",
                    ),
                ),
                html.Li(
                    html.A(
                        "Terraform",
                        href="https://github.com/jyablonski/aws_terraform",
                    ),
                ),
            ]
        ),
        html.H3("Developer"),
        html.P("Jacob Yablonski"),
        html.P(
            [
                "Connect with me on ",
                html.A(
                    html.Img(src="../assets/github.png", height="30px"),
                    href="https://www.linkedin.com/in/jyablonski",
                ),
                " and ",
                html.A(
                    html.Img(src="../assets/linkedin.png", height="30px"),
                    href="https://github.com/jyablonski",
                ),
                html.Br(),
                html.Br(),
                html.A(html.Img(src="../assets/edshot.png", height="150px")),
            ]
        ),
        html.Br(),
        html.P("Version: 0.0.2"),
    ],
    className="custom-padding",
)
