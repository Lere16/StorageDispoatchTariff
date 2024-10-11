import pandas as pd
import os

# Define the folder path where the CSV files are stored
folder_path = 'loads'  # Replace with your folder path

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Use list comprehension to load all CSV files into a list of dataframes
dataframes = [pd.read_csv(os.path.join(folder_path, file), delimiter='\t', na_values=['N/A', 'n/e']) for file in csv_files]

# Combine all dataframes into a single dataframe using pd.concat
combined_df = pd.concat(dataframes, ignore_index=True)

# Display the first few rows of the combined dataframe
print(combined_df.head())

# Save the combined dataframe to a CSV file
combined_df.to_csv('combined_data.csv', index=False)