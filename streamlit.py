import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load the datasets
pop_data_path = "Datasets/ken_rwa_pop.csv"
edu_data_path = "Datasets/ken_rwa_edu.csv"
pop_df = pd.read_csv(pop_data_path)
edu_df = pd.read_csv(edu_data_path)

# Sidebar
st.sidebar.title("Country Selection")
selected_country = st.sidebar.selectbox("Select Country", pop_df['name'].unique())
selected_analysis = st.sidebar.radio("Select Analysis", ["Population", "Education", "Home"])

# Filter the data for the selected country
pop_filtered_df = pop_df[pop_df['name'] == selected_country]
edu_filtered_df = edu_df[edu_df['name'] == selected_country]

# Main app
st.title("Population and Education Analysis Dashboard")

# Summary page
if st.sidebar.button("Home"):
    st.title("Dashboard Summary")
    st.write("Welcome to the Population and Education Analysis Dashboard! This dashboard allows you to explore and analyze population and labor market trends in different countries. You can select a country from the sidebar and choose between two types of analysis: Population Analysis and Education Analysis.")

    st.write("In the Population Analysis:")
    st.write("- You can visualize trends in the total inactive population, total unemployed population, and total employed population over the years.")
    st.write("- You can compare these trends by sex and age group using line plots and bar charts.")
    st.write("- You can also explore IT employment trends by year and gender using a scatter plot.")

    st.write("In the Education Analysis:")
    st.write("- You can view the distribution of education levels by age group using a pie chart.")
    st.write("- You can analyze trends in the total unemployed and employed populations by education level and year.")
    st.write("- You can also investigate labor market trends by education level, unemployment categories, age group, and gender using bar plots.")

    st.write("Feel free to explore different countries, toggle between analyses, and interact with the visualizations to gain insights into population and labor market trends.")

    st.write("Please use the sidebar to get started!")


if selected_analysis == "Population":
    # Set color palette for the plots
    color_palette = px.colors.qualitative.Set1
    
    # Get unique age groups
    age_groups = pop_filtered_df['age_group'].unique()

    # Create a subplot with multiple line plots for each age group
    fig = make_subplots(rows=len(age_groups), cols=1, shared_xaxes=True,
                        subplot_titles=[f"Age Group: {age_group}" for age_group in age_groups])

    for idx, age_group in enumerate(age_groups, start=1):
        age_group_data = pop_filtered_df[pop_filtered_df['age_group'] == age_group]
        
        for sex in age_group_data['sex'].unique():
            sex_data = age_group_data[age_group_data['sex'] == sex]
            
            trace = go.Scatter(x=sex_data['year'], y=sex_data['total_inactive_population'],
                            mode='lines', name=sex)
            
            fig.add_trace(trace, row=idx, col=1)

    # Update subplot layout
    fig.update_layout(title_text=f"Total Inactive Population by Year and Sex ({selected_country})",
                    coloraxis_showscale=False, showlegend=True)

    # Show the figure
    st.plotly_chart(fig)
    
    # Total unemployed population by sex (bar chart)
    fig_unemployed_by_sex = px.bar(pop_filtered_df,
                                   x='sex', y='total_unemployed_population', color = 'age_group',
                                   title=f"Total Unemployed Population by Sex ({selected_country})",
                                   color_discrete_sequence=color_palette)
    st.plotly_chart(fig_unemployed_by_sex)
    
    

    # Get unique age groups
    age_groups = pop_filtered_df['age_group'].unique()

    # Create a subplot with multiple line plots for each age group
    fig = make_subplots(rows=len(age_groups), cols=1, shared_xaxes=True,
                        subplot_titles=[f"Age Group: {age_group}" for age_group in age_groups])

    for idx, age_group in enumerate(age_groups, start=1):
        age_group_data = pop_filtered_df[pop_filtered_df['age_group'] == age_group]
        
        for sex in age_group_data['sex'].unique():
            sex_data = age_group_data[age_group_data['sex'] == sex]
            
            trace = go.Scatter(x=sex_data['year'], y=sex_data['total_employed_population'],
                            mode='lines', name=sex)
            
            fig.add_trace(trace, row=idx, col=1)

    # Update subplot layout
    fig.update_layout(title_text=f"Total Employed Population by Year and Sex ({selected_country})",
                    coloraxis_showscale=False, showlegend=True)

    # Show the figure
    st.plotly_chart(fig)
       
    # Create a scatter plot for IT employment trends
    fig_it_employment_trends = px.bar(pop_filtered_df, x='year', y='Information and communication', color='sex',
                                        title='IT Employment Trends by Year and Gender',
                                        labels={'Information and communication': 'IT Employment'},
                                        hover_name='age_group', hover_data=['population'])

    st.plotly_chart(fig_it_employment_trends)



if selected_analysis == "Education":
    # Education level distribution by age group (pie chart)
    fig_edu_pie = px.pie(edu_filtered_df, names='age_group', values='population',
                         title=f"Education Level Distribution by Age Group ({selected_country})",
                         color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_edu_pie)
    
    # Total unemployed population by education level (bar chart)
    fig_edu_unemployed = px.bar(edu_filtered_df, x='year', y='total_unemployed_population', color='age_group',
                                title=f"Total Unemployed Population by Education Level and Year ({selected_country})",
                                color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_edu_unemployed)
    
    # Total employed population by education level (bar chart)
    fig_edu_employed = px.bar(edu_filtered_df, x='year', y='total_employed_population', color='age_group',
                              title=f"Total Employed Population by Education Level and Year ({selected_country})",
                              color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_edu_employed)

    # Create a new tab for the Education Analysis
    with st.expander("Education Analysis"):
        st.write("Analyzing Labor Market Trends by Education Level and Unemployment Categories")

        # Filter the DataFrame for education-related columns
        edu_filtered_df = edu_filtered_df[['age_group', 'sex', 'Basic_unemployment','Intermediate_unemployment', 'Advanced_unemployment', 'Level not stated_unemployment']]
        
        # Group data by education level, age group, and sex
        edu_age_sex_grouped = edu_filtered_df.groupby(['age_group', 'sex']).sum().reset_index()

        # Create a bar plot for labor market trends by education level, unemployment categories, age group, and sex
        fig_unemployment_by_edu_age_sex = px.bar(edu_age_sex_grouped,
                                                y=['Basic_unemployment', 'Intermediate_unemployment', 'Advanced_unemployment', 'Level not stated_unemployment'],
                                                x='sex', hover_data= ['age_group'], labels={'value': 'Population'},
                                                title="Labor Market Trends by Education Level, Unemployment Categories, Age Group, and Gender",
                                                )
        st.plotly_chart(fig_unemployment_by_edu_age_sex)
