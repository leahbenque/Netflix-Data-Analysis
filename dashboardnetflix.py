import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, dash_table, dcc, callback, Output, Input, html
import dash_mantine_components as dmc

n_topten = pd.read_csv('/Users/leahbenque/Documents/General Assembly - Data Analytics/Python/netflixtopten.csv')

# Create Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={'background-color': '#ffcccb'},  # Ensures background is visible
    children=[
        dmc.Container([
            dmc.Title('Netflix Data Dashboard', color="red"),
            
            # Dropdown 
            dmc.Select(
                label="Select Genre",
                id='genre-dropdown',
                value='All Genres',  # Default
                data=[{'value': 'All Genres', 'label': 'All Genres'}] + 
                     [{'value': genre, 'label': genre} for genre in sorted(n_topten['Genre'].unique())]
            ),
            
            # Layout
            dmc.Grid([
                dmc.Col([dcc.Graph(figure={}, id='scatter-graph')]),
                dmc.Col([dcc.Graph(figure={}, id='histogram-graph')], span=6),
                dmc.Col([dcc.Graph(figure={}, id='barchart-graph')], span=6),
                dmc.Col([dcc.Graph(figure={}, id='boxplot-graph')]),
            ]),

            # Data Table
            dmc.Grid([
                dmc.Col([
                    dash_table.DataTable(data=n_topten.to_dict('records'), page_size=8)
                ], span=12),
            ]),
        ])
    ]
)

# Callback to update all four graphs based on selected genre
@callback(
    [
        Output(component_id='scatter-graph', component_property='figure'),
        Output(component_id='histogram-graph', component_property='figure'),
        Output(component_id='barchart-graph', component_property='figure'),
        Output(component_id='boxplot-graph', component_property='figure')
    ],
    Input(component_id='genre-dropdown', component_property='value')
)  
def update_graphs(selected_genre):
    # Filter data based on the selected genre, all data if "All Genres" is selected
    if selected_genre == 'All Genres':
        filtered_data = n_topten
    else:
        filtered_data = n_topten[n_topten['Genre'] == selected_genre]
    
    # Scatter Plot
    scatter_fig = px.scatter(
        filtered_data,
        x='Runtime',
        y='IMDB Score',
        color='Genre',
        hover_data=['Title', 'Premiere'],
        title=f"IMDB Score VS Runtime for {'All' if selected_genre == 'All Genres' else selected_genre} Movies",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    scatter_fig.update_traces(showlegend=False)
    
    # Histogram
    histogram_fig = px.histogram(
        filtered_data,
        x='IMDB Score',
        nbins=20,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f"IMDB Score Distribution for {'All Genres' if selected_genre == 'All Genres' else selected_genre}"
    )
    
    # Bar Chart
    barchart_fig = px.bar(
        filtered_data.groupby('Language').size().sort_values(ascending=False).reset_index(name='Count'),
        x='Language',
        y='Count',
        title=f"Number of movies in each language for {'All Genres' if selected_genre == 'All Genres' else selected_genre}",
        color='Language',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    barchart_fig.update_traces(showlegend=False)
    
    # Boxplot
    boxplot_fig = px.box(
        filtered_data,
        x='Premiere Year',
        y='Runtime',
        color='Premiere Year',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f"Runtime Distribution for {'All Genres' if selected_genre == 'All Genres' else selected_genre}"
    )
    boxplot_fig.update_traces(showlegend=False)
    
    return scatter_fig, histogram_fig, barchart_fig, boxplot_fig

if __name__ == '__main__':
    app.run(debug=True, port = 8051)