import pandas as pd

# CSV file path
csv_file_path = r'Project\final_data.csv'

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Convert the first 2 rows of the DataFrame to a list (array-like structure)
data_array = df.values.tolist()

#list of skills
skill_columns = df.columns[10:]  

# Dictionary to map each job to its skills
job_skills_dict = {}


# gonna match jobs in array to their skills.
for each in data_array:
    #job title
    job_title = each[2]
    #reset skills
    skills = []

    for iterator in range(10, 41):
        #if skills (like python == 1) is positive
        if each[iterator] == 1:
            skills.append(df.columns[iterator])

    #map job title to list of skills in the dictionary
    job_skills_dict[job_title] = skills