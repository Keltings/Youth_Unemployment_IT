import streamlit as st
import pandas as pd
import plotly.express as px

# Load the DataFrame
data_df = pd.read_csv("Datasets/ken_rwa_edu.csv")  # Replace with your actual dataset file

# Set the page title
st.title("Labor Market Analysis Dashboard")

# Create tabs as cards
tabs = ["Overall Trends", "Employment Trends", "Unemployment Trends", "Employment Distribution"]
selected_tab = st.radio("Select Tab", tabs)

# Sidebar for filters
selected_age_group = st.sidebar.selectbox("Select Age Group", data_df['age_group'].unique())
selected_sex = st.sidebar.selectbox("Select Sex", data_df['sex'].unique())
selected_country = st.sidebar.selectbox("Select Country", data_df['name'].unique())

# Filter the data based on selected filters
filtered_df = data_df[
    (data_df['age_group'] == selected_age_group) &
    (data_df['sex'] == selected_sex) &
    (data_df['name'] == selected_country)
]

# Display basic information
st.write(f"Selected Age Group: {selected_age_group}")
st.write(f"Selected Sex: {selected_sex}")
st.write(f"Selected Country: {selected_country}")
st.write(f"Total Entries: {len(filtered_df)}")

# Show selected tab content
if selected_tab == "Overall Trends":
    st.subheader("Overall Employment Trends")
    fig_line = px.line(filtered_df, x='year', y='total_employed_population', title="Overall Employment Trends")
    st.plotly_chart(fig_line)

elif selected_tab == "Employment Trends":
    st.subheader("Employment and Unemployment Trends")
    fig_bar = px.bar(filtered_df, x='year', y=['total_employed_population', 'total_unemployed_population'],
                     title="Employment and Unemployment Trends")
    st.plotly_chart(fig_bar)

elif selected_tab == "Unemployment Trends":
    st.subheader("Unemployment Trends")
    fig_line_unemployment = px.line(filtered_df, x='year', y='total_unemployed_population', title="Unemployment Trends")
    st.plotly_chart(fig_line_unemployment)

elif selected_tab == "Employment Distribution":
    st.subheader("Employment Distribution")
    fig_pie = px.pie(filtered_df, names='year', values='total_employed_population',
                     title="Employment Distribution by Year")
    st.plotly_chart(fig_pie)
