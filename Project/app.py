import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit as st

# Load the dataset
df = pd.read_csv(r'Project\postings.csv')

# Clean the dataset: Remove unnecessary columns, handle missing values, etc.
df['original_listed_time'] = pd.to_datetime(df['original_listed_time'], unit='ms')
df['expiry'] = pd.to_datetime(df['expiry'], unit='ms')

# Handle missing salary values (if necessary)
df = df.dropna(subset=['max_salary', 'min_salary'])

# Convert salary columns to numeric values
df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce')
df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce')

# Clean 'formatted_work_type' column
df['formatted_work_type'] = df['formatted_work_type'].str.strip().str.title()


# Set up the app title
st.title('Job Posting Insights')

# Sidebar for filtering
st.sidebar.header("Filter Jobs")

# Filter by job title
job_title_filter = st.sidebar.text_input('Enter Job Title (e.g., "Marketing Coordinator")', '')

# Filter by company
company_filter = st.sidebar.text_input('Enter Company Name', '')

# Filter by location
location_filter = st.sidebar.text_input('Enter Location (e.g., "Princeton, NJ")', '')

# Filter by salary range
salary_min = st.sidebar.slider('Minimum Salary', 0, 200000, 0)
salary_max = st.sidebar.slider('Maximum Salary', 0, 200000, 200000)

# Filter by work type
work_type = st.sidebar.selectbox('Work Type', ['All', 'Full-time', 'Part-time'])

# Filter by experience level
experience_level = st.sidebar.selectbox('Experience Level', ['All', 'Entry', 'Mid', 'Senior'])

# Filter the dataframe based on user input
filtered_df = df

if filtered_df.shape[0] > 0:
    # Display filtered results
    st.subheader(f"Found {filtered_df.shape[0]} job postings")

    # Show a preview of the filtered jobs
    st.write(filtered_df[['title', 'company_name', 'location', 'min_salary', 'max_salary', 'formatted_work_type']].head(10))

    # Display detailed information about the selected job posting
    st.subheader("Job Posting Details")
    job_id = st.number_input(
        "Enter Job ID to View Details", 
        min_value=0, 
        max_value=int(filtered_df.shape[0]) - 1,  # Ensure max_value is within bounds
        step=1
    )

if job_title_filter:
    filtered_df = filtered_df[filtered_df['title'].str.contains(job_title_filter, case=False, na=False)]
if company_filter:
    filtered_df = filtered_df[filtered_df['company_name'].str.contains(company_filter, case=False, na=False)]
if location_filter:
    filtered_df = filtered_df[filtered_df['location'].str.contains(location_filter, case=False, na=False)]
if salary_min > 0:
    filtered_df = filtered_df[filtered_df['max_salary'] >= salary_min]
if salary_max < 200000:
    filtered_df = filtered_df[filtered_df['min_salary'] <= salary_max]
if work_type != 'All':
    filtered_df = filtered_df[filtered_df['formatted_work_type'] == work_type]
if experience_level != 'All':
    filtered_df = filtered_df[filtered_df['formatted_experience_level'] == experience_level]

# Display filtered results
st.subheader(f"Found {filtered_df.shape[0]} job postings")

# Show a preview of the filtered jobs
st.write(filtered_df[['title', 'company_name', 'location', 'min_salary', 'max_salary', 'formatted_work_type']].head(10))

# Display detailed information about the selected job posting
st.subheader("Job Posting Details")
job_id = st.number_input("Enter Job ID to View Details", min_value=0, max_value=int(filtered_df.shape[0]) - 1, step=1)
if job_id >= 0:
    job_detail = filtered_df.iloc[job_id]
    st.write(f"**Job Title:** {job_detail['title']}")
    st.write(f"**Company:** {job_detail['company_name']}")
    st.write(f"**Location:** {job_detail['location']}")
    st.write(f"**Description:** {job_detail['description']}")
    st.write(f"**Salary Range:** ${job_detail['min_salary']} - ${job_detail['max_salary']}")
    st.write(f"**Work Type:** {job_detail['formatted_work_type']}")
else:
    st.write("No jobs found matching the selected filters.")

# Job Titles Distribution
st.subheader('Top Job Titles Distribution')
top_job_titles = filtered_df['title'].value_counts().head(10)
fig = px.bar(x=top_job_titles.index, y=top_job_titles.values, labels={'x': 'Job Title', 'y': 'Number of Postings'})
st.plotly_chart(fig)

# Average Salary by Location
st.subheader('Average Salary by Location')
avg_salary_by_location = filtered_df.groupby('location')[['max_salary', 'min_salary']].mean()
fig = px.bar(avg_salary_by_location, x=avg_salary_by_location.index, y='max_salary',
             labels={'max_salary': 'Average Max Salary', 'index': 'Location'},
             title='Average Maximum Salary by Location')
st.plotly_chart(fig)

# Job Postings Over Time
st.subheader('Job Postings Over Time')
df['listed_month'] = df['original_listed_time'].dt.to_period('M')
job_postings_per_month = df.groupby('listed_month').size()
fig = px.line(job_postings_per_month, x=job_postings_per_month.index.astype(str), y=job_postings_per_month.values,
              labels={'x': 'Month', 'y': 'Number of Postings'}, title='Job Postings Trends Over Time')
st.plotly_chart(fig)

