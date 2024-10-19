import pandas as pd

#csv file
csv_file_path = 'FA24-Group19\Project\output.csv'

#read file
df = pd.read_csv(csv_file_path)

print("\nFirst 500 rows:")
print(df.head(500))