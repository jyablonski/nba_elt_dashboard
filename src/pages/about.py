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
        html.P(
            "All NBA Game log, schedule, standings, and play-by-play data is webscraped daily from"
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
                html.A(
                    html.Img(src="../assets/edshot.png", height="150px"),
                    href="https://github.com/jyablonski",
                ),
            ]
        ),
    ],
    className="custom-padding",
)
