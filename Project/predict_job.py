# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Step 2: Load the dataset
# Ensure to replace with your actual dataset file path
data = pd.read_csv('Project\postings.csv', encoding='utf-8')

# Display the first few rows of the dataset
print(data.head())

# Step 3: Data Preprocessing
# Handle missing values
data = data.dropna(subset=['title', 'description', 'max_salary'])

# Convert salary to numeric (some may have commas or other symbols, we will clean those)
data['max_salary'] = pd.to_numeric(data['max_salary'], errors='coerce')

# Remove rows where salary is NaN after conversion
data = data.dropna(subset=['max_salary'])

# Clean job descriptions (optional)
def clean_text(text):
    text = text.lower()  # Lowercase the text
    text = re.sub(r'[^a-z\s]', '', text)  # Keep only alphabets and spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

data['cleaned_description'] = data['description'].apply(clean_text)

# Encode job titles and locations
label_encoder = LabelEncoder()
data['title_encoded'] = label_encoder.fit_transform(data['title'])
data['location_encoded'] = label_encoder.fit_transform(data['location'].fillna('Unknown'))  # Handle missing locations

# Step 4: Feature Engineering
# Features to use for the prediction model
X = data[['title_encoded', 'location_encoded', 'cleaned_description']]

# Target variable: salary
y = data['max_salary']

# Step 5: Text Vectorization using TF-IDF for the job description
# We will use a ColumnTransformer to apply TF-IDF only on the 'cleaned_description'
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)  # Limit the features to 5000 to avoid overfitting

# Step 6: Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Model Building - Random Forest Regressor
# We create a pipeline to apply transformations and fit the regression model
pipeline = make_pipeline(
    ColumnTransformer(
        transformers=[
            ('desc', vectorizer, 'cleaned_description'),  # Apply TF-IDF on job description
            ('cat', StandardScaler(), ['title_encoded', 'location_encoded'])  # Standardize title and location encoded columns
        ]
    ),
    RandomForestRegressor(n_estimators=100, random_state=42)  # Using RandomForestRegressor
)

# Step 8: Training the Model
pipeline.fit(X_train, y_train)

# Step 9: Make Predictions
y_pred = pipeline.predict(X_test)

# Step 10: Evaluate the Model
# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# R² (R-squared) Score
r2 = r2_score(y_test, y_pred)
print(f"R² (R-squared): {r2:.4f}")

# Step 11: Predict Salary for a New Job Posting
# Step 11: Predict Salary for a New Job Posting

# New job data for prediction
new_job_description = ["We are looking for a senior software engineer with extensive experience in Python, Django, and machine learning."]
new_title = ['Software Engineer']  # New job title that wasn't in the training data
new_location = ['San Francisco, CA']  # New job location

# First, we fit the LabelEncoder again on the combined dataset of existing titles and the new title
combined_titles = data['title'].tolist() + new_title  # Combine old titles with new title
label_encoder_title = LabelEncoder()
label_encoder_title.fit(combined_titles)

# Encode the new title
new_title_encoded = label_encoder_title.transform(new_title)

# Encode the location (for unseen location handling)
combined_locations = data['location'].dropna().tolist() + new_location  # Combine old locations with new location
label_encoder_location = LabelEncoder()
label_encoder_location.fit(combined_locations)

# Encode the new location
new_location_encoded = label_encoder_location.transform(new_location)

# Clean the new job description
new_description_cleaned = [clean_text(desc) for desc in new_job_description]

# Create a DataFrame for new data
new_data = pd.DataFrame({
    'title_encoded': new_title_encoded,
    'location_encoded': new_location_encoded,
    'cleaned_description': new_description_cleaned
})

# Predict the salary for the new job posting
predicted_salary = pipeline.predict(new_data)
print(f"Predicted Salary for the new job posting: ${predicted_salary[0]:,.2f}")
print("Done")