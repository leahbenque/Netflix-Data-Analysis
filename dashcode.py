import pandas as pd
import plotly.express as px
import streamlit as st

# Load dataset
n_topten = pd.read_csv('netflixtoptenfiltered.csv')

# Streamlit App Configuration
st.set_page_config(page_title="Netflix Data Dashboard", layout="wide")

# Title
st.title("Netflix Data Dashboard")

# Sidebar for Genre Selection
st.sidebar.header("Filter Options")
selected_genre = st.sidebar.selectbox(
    "Select Genre", 
    ["All Genres"] + sorted(n_topten["Genre"].unique())
)

# Filter the data based on selected genre
filtered_data = n_topten if selected_genre == "All Genres" else n_topten[n_topten["Genre"] == selected_genre]

# Layout for graphs
col1, col2 = st.columns(2)

# Scatter Plot
with col1:
    st.subheader(f"IMDB Score vs Runtime for {selected_genre} Movies")
    scatter_fig = px.scatter(
        filtered_data,
        x="Runtime",
        y="IMDB Score",
        color="Genre",
        hover_data=["Title", "Premiere"],
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    scatter_fig.update_traces(showlegend=False)
    st.plotly_chart(scatter_fig, use_container_width=True)

# Histogram
with col2:
    st.subheader(f"IMDB Score Distribution for {selected_genre}")
    histogram_fig = px.histogram(
        filtered_data,
        x="IMDB Score",
        nbins=20,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(histogram_fig, use_container_width=True)

# Bar Chart
st.subheader(f"Number of Movies in Each Language for {selected_genre}")
barchart_fig = px.bar(
    filtered_data.groupby("Language").size().sort_values(ascending=False).reset_index(name="Count"),
    x="Language",
    y="Count",
    color="Language",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
barchart_fig.update_traces(showlegend=False)
st.plotly_chart(barchart_fig, use_container_width=True)

# Boxplot
st.subheader(f"Runtime Distribution for {selected_genre}")
boxplot_fig = px.box(
    filtered_data,
    x="Premiere Year",
    y="Runtime",
    color="Premiere Year",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
boxplot_fig.update_traces(showlegend=False)
st.plotly_chart(boxplot_fig, use_container_width=True)

# Data Table
st.subheader("Netflix Top Ten Data")
st.dataframe(filtered_data)

# Run app (for local execution)
if __name__ == "__main__":
    pass
