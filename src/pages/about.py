from datetime import datetime

from dash import html

about_layout = html.Div(
    [
        html.Link(
            rel="stylesheet",
            href="../assets/styles.css",
        ),
        html.H1("About this Project", style={"text-align": "left"}),
        html.P(
            [
                "This dashboard shows up to date information about the current NBA Season. "
                "It's built with Dash, hosted on cloud infrastructure, and routed through AWS Route 53 "
                "for custom domain management.",
                html.Br(),
                html.Br(),
                "For more details, visit the internal ",
                html.A(
                    "Documentation Site",
                    href="https://doqs.jyablonski.dev",
                ),
            ]
        ),
        html.H2("Data"),
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
                    "A custom Logistic Regression ML Model is used to provide Win % Predictions \
                    in the Schedule Tab"
                ),
            ]
        ),
        html.H2("Project Infrastructure"),
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
                        href="https://github.com/jyablonski/nba_elt_ingestion",
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
                        "Terraform",
                        href="https://github.com/jyablonski/aws_terraform",
                    ),
                ),
                html.Li(
                    html.A(
                        "Internal Documentation",
                        href="https://github.com/jyablonski/doqs",
                    ),
                ),
            ]
        ),
        html.H2("Developer"),
        html.P("Jacob Yablonski"),
        html.P(
            [
                "Connect with me on ",
                html.A(
                    html.Img(src="../assets/linkedin.png", height="30px"),
                    href="https://www.linkedin.com/in/jacobyablonski",
                ),
                " and ",
                html.A(
                    html.Img(src="../assets/github.png", height="30px"),
                    href="https://github.com/jyablonski",
                ),
                html.Br(),
                html.Br(),
                html.A(html.Img(src="../assets/edshot.png", height="150px")),
            ]
        ),
        html.Br(),
        html.P(
            f"Dashboard Last Refreshed {datetime.now().strftime('%A, %B %d %-I:%M %p UTC')}"
        ),
        html.P("Version: 1.1.6"),
    ],
    className="custom-padding",
)
