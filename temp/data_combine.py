import pandas as pd
import glob, os

# Specify the folder containing the CSV files
folder_path = 'prices/'

# Read all CSV files in the folder
all_files = glob.glob(folder_path + "*.csv")

# Create a list to hold the dataframes
dataframes = []

for filename in all_files:
    df = pd.read_csv(filename)
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
result = pd.concat(dataframes, ignore_index=True)

# Save the resulting dataframe to a new CSV file
result_file_path = os.path.join(folder_path, 'compiled_price.csv')
result.to_csv(result_file_path, index=False)
