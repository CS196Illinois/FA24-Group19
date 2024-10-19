import pandas as pd

# CSV file path
csv_file_path = r'FA24-Group19\Project\output.csv'

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Convert the first 2 rows of the DataFrame to a list (array-like structure)
data_array = df.head(50).values.tolist()

# Print the resulting array
print(data_array)

#"Software Engineer", "Data Scientist", "Researcher", "Web Developer", 
#   "UI/UX Designer", "Teacher", "Full Stack Developer", "Mobile Developer", "Cybersecurity"