import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, callback, Output, Input, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

# Load dataset
n_topten = pd.read_csv('netflixtopten.csv')

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dmc.Container(
    [
        dmc.Title("Netflix Data Dashboard", c="red"),

        # Dropdown
        dmc.Select(
            label="Select Genre",
            id="genre-dropdown",
            value="All Genres",
            data=[{"value": "All Genres", "label": "All Genres"}]
            + [{"value": genre, "label": genre} for genre in sorted(n_topten["Genre"].unique())],
        ),

        # Grid Layout for Graphs
        dmc.Grid(
            [
                dmc.Grid.Col(dcc.Graph(figure={}, id="scatter-graph"), span=6),
                dmc.Grid.Col(dcc.Graph(figure={}, id="histogram-graph"), span=6),
                dmc.Grid.Col(dcc.Graph(figure={}, id="barchart-graph"), span=6),
                dmc.Grid.Col(dcc.Graph(figure={}, id="boxplot-graph"), span=6),
            ]
        ),

        # Data Table
        dmc.Grid(
            [
                dmc.Grid.Col(
                    dash_table.DataTable(data=n_topten.to_dict("records"), page_size=8),
                    span=12,
                ),
            ]
        ),
    ],
    fluid=True,
)

# Callback to update graphs
@callback(
    [
        Output("scatter-graph", "figure"),
        Output("histogram-graph", "figure"),
        Output("barchart-graph", "figure"),
        Output("boxplot-graph", "figure"),
    ],
    Input("genre-dropdown", "value"),
)
def update_graphs(selected_genre):
    # Filter data based on the selected genre
    filtered_data = n_topten if selected_genre == "All Genres" else n_topten[n_topten["Genre"] == selected_genre]

    # Scatter Plot
    scatter_fig = px.scatter(
        filtered_data,
        x="Runtime",
        y="IMDB Score",
        color="Genre",
        hover_data=["Title", "Premiere"],
        title=f"IMDB Score vs Runtime for {selected_genre} Movies",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    scatter_fig.update_traces(showlegend=False)

    # Histogram
    histogram_fig = px.histogram(
        filtered_data,
        x="IMDB Score",
        nbins=20,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f"IMDB Score Distribution for {selected_genre}",
    )

    # Bar Chart
    barchart_fig = px.bar(
        filtered_data.groupby("Language").size().sort_values(ascending=False).reset_index(name="Count"),
        x="Language",
        y="Count",
        title=f"Number of Movies in Each Language for {selected_genre}",
        color="Language",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    barchart_fig.update_traces(showlegend=False)

    # Boxplot
    boxplot_fig = px.box(
        filtered_data,
        x="Premiere Year",
        y="Runtime",
        color="Premiere Year",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f"Runtime Distribution for {selected_genre}",
    )
    boxplot_fig.update_traces(showlegend=False)

    return scatter_fig, histogram_fig, barchart_fig, boxplot_fig


# Run app (for local execution)
if __name__ == "__main__":
    app.run(debug=True, port=8050)
