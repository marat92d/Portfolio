

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
fig = go.Figure()


df = pd.read_csv("games.csv")
df = df.dropna()
df = df.query("Year_of_Release >= 2000")
df.Year_of_Release = df.Year_of_Release.astype(int)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="История игровой индустрии", className="header-title",
                        style={"fontSize": "48px", "color": "#00361c",
                               'padding': 10, 'flex': 1, 'text-align': 'center'}),
                html.P(
                    children="Сравнение игр выпущенных на различных платформах и их оценки за последние 15 лет",
                    className="header-description",
                    style={"fontSize": "36px", "color": "#17B897", 'padding': 10, 'flex': 1, 'text-align': 'center'}
                ),

            ], className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Жанр", className="menu-title"),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[
                                {"label": genre, "value": genre}
                                for genre in np.sort(df.Genre.unique())
                            ],
                            value=["Sports", 'Action'],
                            clearable=False,
                            className="dropdown",
                            multi=True,
                        ),
                    ], style={'width': '45%', 'display': 'inline-block', "color": "#00361c", "fontSize": "24px",
                              'padding': 10, 'flex': 1}

                ),
                html.Div(
                    children=[
                        html.Div(children="Рейтинг", className="menu-title"),
                        dcc.Dropdown(
                            id="rating-filter",
                            options=[
                                {"label": rating, "value": rating}
                                for rating in df.Rating.unique()
                            ],
                            value="E",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                            multi=True,
                        ),
                    ], style={'width': '45%', 'display': 'inline-block', "color": "#00361c", "fontSize": "24px"}
                ),

            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="area-chart", config={"displayModeBar": False},
                    ),
                    className="card", style={'width': '45%', 'height': '300px'}
                ),
                html.Div(
                    children=dcc.Graph(
                        id="scatter-chart", config={"displayModeBar": False},
                    ),
                    className="card", style={'width': '45%', 'display': 'inline-block'}
                ),
                html.Div(
                    children=dcc.Graph(
                        id="indicator-chart", config={"displayModeBar": False},
                    ),
                    className="card", style={'width': '45%', 'display': 'inline-block'}
                ),


            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                html.Div(
                    children="Временной период",
                    className="menu-title"
                ),
                dcc.RangeSlider(
                    min=df.Year_of_Release.min(),
                    max=df.Year_of_Release.max(),
                    value=[2000, 2009],
                    id="year-range",
                    step=1,
                    marks={i: str(i) for i in range(df.Year_of_Release.min(), df.Year_of_Release.max() + 1, 1)}


                ),

            ], style={'width': '90%', "color": "black", "fontSize": "24px",
                      'padding': 10, 'flex': 1, 'margin-bottom': 30, }
        ),

    ]
)


@app.callback(
    [Output("area-chart", "figure"), Output("scatter-chart", "figure"), Output("indicator-chart", "figure")],
    [
        Input("genre-filter", "value"),
        Input("rating-filter", "value"),
        Input("year-range", "value"),
    ],
)
def update_charts(genre, rating, value):
    filtered_data = df[df.Genre.isin(list(genre))]

    filtered_data = filtered_data[filtered_data.Rating.isin(list(rating))]

    filtered_data = filtered_data.loc[(filtered_data.Year_of_Release >= value[0])
                                      & (filtered_data.Year_of_Release <= value[1])]

    df_area = filtered_data.groupby(['Year_of_Release', 'Platform']).count().reset_index()

    area_chart_figure = px.area(
        df_area, x="Year_of_Release", y="Name", labels={
            "Year_of_Release": "Год",
            "Name": "Количество",
        },
        color="Platform")

    scatter_chart_figure = px.scatter(filtered_data, x="User_Score", y="Critic_Score", color="Genre"
                                      , labels={
            "User_Score": "Оценки игроков",
            "Critic_Score": "Оценки критиков",
        }, )

    fig = go.Figure(go.Indicator(
        mode="number",
        value=filtered_data.Name.count(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Количество выбранных игр"}))

    return fig, area_chart_figure, scatter_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True,
                   host = '127.0.0.1')












