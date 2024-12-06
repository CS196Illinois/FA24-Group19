import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit as st

# Load the dataset
# Reader can download postings.csv from https://www.kaggle.com/datasets/arshkon/linkedin-job-postings?select=postings.csv
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

# Clean 'formatted_experience_type' column
df['formatted_experience_level'] = df['formatted_experience_level'].str.strip().str.title()

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
work_type = st.sidebar.selectbox('Work Type', ['All', 'Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary', 'Other'])

# Filter by experience level
experience_level = st.sidebar.selectbox('Experience Level', ['All', 'Internship', 'Entry Level', 'Mid-Senior Level', 'Associate', 'Executive', 'Director'])

# Filter the dataframe based on user input
filtered_df = df

if filtered_df.shape[0] > 0:
    # Display filtered results
    st.subheader(f"Found {filtered_df.shape[0]} job postings")

    # Show a preview of the filtered jobs
    st.write(filtered_df[['title', 'company_name', 'location', 'min_salary', 'max_salary', 'formatted_work_type', 'formatted_experience_level']].head(10))

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
    filtered_df = filtered_df[filtered_df['formatted_work_type'].str.title() == work_type.title()]
if experience_level != 'All':
    filtered_df = filtered_df[filtered_df['formatted_experience_level'].str.title() == experience_level.title()]

# Display filtered results
st.subheader(f"Found {filtered_df.shape[0]} job postings")

# Show a preview of the filtered jobs
st.write(filtered_df[['title', 'company_name', 'location', 'min_salary', 'max_salary', 'formatted_work_type', 'formatted_experience_level']].head(10))

# Initialize session state for navigation
if 'start_index' not in st.session_state:
    st.session_state['start_index'] = 0

# Define the number of jobs to display per page
jobs_per_page = 10

# Get the current page of jobs
start_idx = st.session_state['start_index']
end_idx = start_idx + jobs_per_page
current_page_df = filtered_df.iloc[start_idx:end_idx]

# Display current page of jobs
st.subheader(f"Displaying jobs {start_idx + 1} to {min(end_idx, filtered_df.shape[0])} of {filtered_df.shape[0]}")
st.write(current_page_df[['title', 'company_name', 'location', 'min_salary', 'max_salary', 'formatted_work_type', 'formatted_experience_level']])

# Navigation buttons under the job postings
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Previous"):
        if st.session_state['start_index'] > 0:
            st.session_state['start_index'] -= jobs_per_page

with col2:
    st.write("")  # Empty space for better alignment

with col3:
    if st.button("Next"):
        if st.session_state['start_index'] + jobs_per_page < filtered_df.shape[0]:
            st.session_state['start_index'] += jobs_per_page

job_id_counter = 0
# Display detailed information about the selected job posting
# Check if filtered_df has rows before creating number_input
if not current_page_df.empty:
    
    # Display detailed information about the selected job posting
    st.subheader("Job Posting Details")
    job_id = st.number_input(
        "Enter Job ID to View Details",
        min_value=0,
        max_value=int(filtered_df.shape[0]) - 1,  # Ensure max_value is valid
        step=1,
        key=job_id_counter
    )

    # Increment the counter for subsequent widgets
    job_id_counter += 1

    # Display job details for the selected ID
    job_detail = filtered_df.iloc[job_id]
    st.write(f"**Job Title:** {job_detail['title']}")
    st.write(f"**Company:** {job_detail['company_name']}")
    st.write(f"**Location:** {job_detail['location']}")
    st.write(f"**Description:** {job_detail['description']}")
    st.write(f"**Salary Range:** ${job_detail['min_salary']} - ${job_detail['max_salary']}")
    st.write(f"**Work Type:** {job_detail['formatted_work_type']}")
    st.write(f"**Experience Level:** {job_detail['formatted_experience_level']}")
else:
    # Display a message if no jobs match the filters
    st.write("No jobs found matching the selected filters.")

# Job Titles Distribution
st.subheader('Top Job Titles Distribution')
top_job_titles = filtered_df['title'].value_counts().head(10)
# Job Titles Distribution
st.subheader('Top Job Titles Distribution')
top_job_titles = filtered_df['title'].value_counts().head(10)

# Convert to DataFrame for Plotly
top_job_titles_df = top_job_titles.reset_index()
top_job_titles_df.columns = ['Job Title', 'Number of Postings']

# Create the bar chart
fig = px.bar(
    top_job_titles_df,
    x='Job Title',
    y='Number of Postings',
    labels={'Job Title': 'Job Title', 'Number of Postings': 'Number of Postings'},
    title='Top Job Titles Distribution'
)
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

