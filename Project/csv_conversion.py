import json
import pandas as pd

# Read JSON data from the file
with open('us_person_profile.txt', 'r') as file:
    data = [json.loads(line) for line in file]

# Flattening function for experiences and education
def flatten_profile(profile):
    # Extract base information
    base_info = {
        "public_identifier": profile.get("public_identifier"),
        "first_name": profile.get("first_name"),
        "last_name": profile.get("last_name"),
        "occupation": profile.get("occupation"),
        "country": profile.get("country"),
        "city": profile.get("city"),
        "connections": profile.get("connections"),
        "experiences": profile.get("experiences"),
        "education": profile.get("education"),
    }
    
    # Flatten experiences
    experiences = profile.get("experiences", [])
    flattened_experiences = []
    for exp in experiences:
        exp_info = {
            "company": exp.get("company"),
            "title": exp.get("title"),
            "starts_at": exp.get("starts_at"),
            "ends_at": exp.get("ends_at"),
            "location": exp.get("location"),
        }
        flattened_experiences.append(exp_info)

    # Flatten education
    education = profile.get("education", [])
    flattened_education = []
    for edu in education:
        edu_info = {
            "school": edu.get("school"),
            "degree_name": edu.get("degree_name"),
            "field_of_study": edu.get("field_of_study"),
        }
        flattened_education.append(edu_info)
    
    # Combine everything into a single record
    record = base_info.copy()
    record['experiences'] = flattened_experiences
    record['education'] = flattened_education
    
    return record

# Flatten all profiles
flattened_data = [flatten_profile(profile) for profile in data]

# Create a DataFrame and save to CSV
df = pd.json_normalize(flattened_data, 
                       record_path=['experiences'], 
                       meta=['public_identifier', 'first_name', 'last_name', 'occupation', 'country', 'city', 'connections'])

# Save to CSV
df.to_csv('output.csv', index=False)

print("CSV conversion complete!")
print(df)

