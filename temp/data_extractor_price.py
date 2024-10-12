import pandas as pd

# Load the CSV file
year=2023
file_path = 'prices/price2023.csv'   # Replace with the path to your CSV file
df = pd.read_csv(file_path)

# Convert the 'Time' column to datetime and create a new 'Start_Time' column
df['Time'] = pd.to_datetime(df['MTU (CET/CEST)'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')

# Filter for rows where the minute is 00 (i.e., on the hour)
hourly_data = df[df['Time'].dt.minute == 0]

# Drop unnecessary columns
hourly_data = hourly_data[['Time', 'Day-ahead Price [EUR/MWh]', 'Currency']]

# Rename columns for clarity
hourly_data.columns = ['Time', 'Day-ahead Price [EUR/MWh]', 'Currency']

# Save the result to a new CSV file
hourly_data.to_csv(f"hourly_DA_price_{year}.csv", index=False)

# Display the first few rows of the filtered data
print(hourly_data.head())
