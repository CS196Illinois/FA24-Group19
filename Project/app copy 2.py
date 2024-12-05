import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Load the dataset
df = pd.read_csv('postings.csv')

# Clean the dataset: Convert timestamps, handle missing values, etc.
df['original_listed_time'] = pd.to_datetime(df['original_listed_time'], unit='ms')
df['expiry'] = pd.to_datetime(df['expiry'], unit='ms')

# Handle missing salary values by removing rows with NaN salaries
df = df.dropna(subset=['max_salary', 'min_salary'])

# Convert salary columns to numeric values, forcing errors to NaN
df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce')
df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce')

# Clean 'formatted_work_type' column (strip whitespace and standardize case)
df['formatted_work_type'] = df['formatted_work_type'].str.strip().str.title()

# Set up the app title
st.title('Job Posting Insights')

# Sidebar for filtering
st.sidebar.header("Filter Jobs")

# Filter by job title
job_title_filter = st.sidebar.text_input('Enter Job Title (e.g., "Marketing Coordinator")', key='job_title_filter')

# Filter by company
company_filter = st.sidebar.text_input('Enter Company Name', key='company_filter')

# Filter by location
location_filter = st.sidebar.text_input('Enter Location (e.g., "Princeton, NJ")', key='location_filter')

# Filter by salary range
salary_min = st.sidebar.slider('Minimum Salary', 0, 200000, 0, key='salary_min')
salary_max = st.sidebar.slider('Maximum Salary', 0, 200000, 200000, key='salary_max')

# Ensure salary_min is less than or equal to salary_max
if salary_min > salary_max:
    salary_min, salary_max = salary_max, salary_min

# Filter by work type
work_type = st.sidebar.selectbox('Work Type', ['All', 'Full-time', 'Part-time'], key='work_type')

# Filter by experience level
experience_level = st.sidebar.selectbox('Experience Level', ['All', 'Entry', 'Mid', 'Senior'], key='experience_level')

# Filter by description keyword
description_keyword = st.sidebar.text_input('Keyword in Description (optional)', key='description_keyword')

# Apply filters to the dataframe
filtered_df = df.copy()

# Job title filter
if job_title_filter:
    filtered_df = filtered_df[filtered_df['title'].str.contains(job_title_filter, case=False, na=False)]

# Company filter
if company_filter:
    filtered_df = filtered_df[filtered_df['company_name'].str.contains(company_filter, case=False, na=False)]

# Location filter
if location_filter:
    filtered_df = filtered_df[filtered_df['location'].str.contains(location_filter, case=False, na=False)]

# Salary filter
if salary_min > 0:
    filtered_df = filtered_df[filtered_df['min_salary'] >= salary_min]
if salary_max < 200000:
    filtered_df = filtered_df[filtered_df['max_salary'] <= salary_max]

# Work type filter
if work_type != 'All':
    filtered_df = filtered_df[filtered_df['formatted_work_type'] == work_type]

# Experience level filter
if experience_level != 'All':
    filtered_df = filtered_df[filtered_df['experience_level'] == experience_level]

# Description keyword filter (if provided)
if description_keyword:
    filtered_df = filtered_df[filtered_df['description'].str.contains(description_keyword, case=False, na=False)]

# Display filtered results
st.subheader(f"Found {filtered_df.shape[0]} job postings")

# Show a preview of the filtered jobs
# Display detailed information about the selected job posting
st.subheader("Job Posting Details")

# Ensure there are jobs available after filtering
# Display detailed information about the selected job posting
st.subheader("Job Posting Details")

# Ensure there are jobs available after filtering
if filtered_df.shape[0] > 0:
    # Only show the number input if there are job postings
    job_id = st.number_input(
        "Enter Job ID to View Details",
        min_value=0,
        max_value=filtered_df.shape[0] - 1,  # Ensure max_value is valid only if there are jobs
        step=1,
        key='job_id_input'
    )

    # Ensure job_id is within valid range
    if 0 <= job_id < filtered_df.shape[0]:
        job_detail = filtered_df.iloc[job_id]
        st.write(f"**Job Title:** {job_detail['title']}")
        st.write(f"**Company:** {job_detail['company_name']}")
        st.write(f"**Location:** {job_detail['location']}")
        st.write(f"**Description:** {job_detail['description']}")
        st.write(f"**Salary Range:** ${job_detail['min_salary']} - ${job_detail['max_salary']}")
        st.write(f"**Work Type:** {job_detail['formatted_work_type']}")
    else:
        st.write("Invalid job selection.")
else:
    st.write("No jobs found matching your filters.")



# Top Job Titles Distribution
st.subheader('Top Job Titles Distribution')
top_job_titles = filtered_df['title'].value_counts().head(10)
fig = px.bar(x=top_job_titles.index, y=top_job_titles.values,
             labels={'x': 'Job Title', 'y': 'Number of Postings'},
             title='Top Job Titles Distribution')
st.plotly_chart(fig)

# Average Salary by Location
st.subheader('Average Salary by Location')
avg_salary_by_location = filtered_df.groupby('location')[['max_salary', 'min_salary']].mean().reset_index()
fig = px.bar(avg_salary_by_location, x='location', y='max_salary',
             labels={'max_salary': 'Average Max Salary', 'location': 'Location'},
             title='Average Maximum Salary by Location')
st.plotly_chart(fig)

# Job Postings Over Time
st.subheader('Job Postings Over Time')
df['listed_month'] = df['original_listed_time'].dt.to_period('M')
job_postings_per_month = df.groupby('listed_month').size().reset_index(name='count')
job_postings_per_month['listed_month'] = job_postings_per_month['listed_month'].astype(str)
fig = px.line(job_postings_per_month, x='listed_month', y='count',
              labels={'listed_month': 'Month', 'count': 'Number of Postings'},
              title='Job Postings Trends Over Time')
st.plotly_chart(fig)

# Top Companies by Number of Job Postings
st.subheader('Top Companies by Number of Job Postings')
top_companies = filtered_df['company_name'].value_counts().head(10)
fig = px.bar(x=top_companies.index, y=top_companies.values,
             labels={'x': 'Company', 'y': 'Number of Postings'},
             title='Top Companies by Number of Job Postings')
st.plotly_chart(fig)
