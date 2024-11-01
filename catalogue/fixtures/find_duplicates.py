import pandas as pd

# Load the CSV file into a DataFrame
file_path = '~/development/milestone_project_4/catalogue/fixtures/sample_dataset.csv'  # Update with your CSV file path
df = pd.read_csv(file_path)

# Identify and keep only the unique rows
df_no_duplicates = df.drop_duplicates()

# Save the cleaned DataFrame back to a new CSV file
df_no_duplicates.to_csv('./cleaned_dataset.csv', index=False)

print(f"Removed duplicates. Cleaned file saved as 'cleaned_file.csv'.")

