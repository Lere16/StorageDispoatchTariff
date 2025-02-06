def detect_hyphen_values(df):
    """
    Détecte les colonnes contenant des cellules avec uniquement le caractère '-'.
    """
    problematic_columns = {}

    for col in df.columns:
        # Vérifier si la colonne contient des valeurs "-"
        mask = df[col].astype(str) == "-"
        if mask.any():
            problematic_columns[col] = df[col][mask].count()  # Nombre d'occurrences

    return problematic_columns


#check DE/LU data 
import pandas as pd
import numpy as np
import os 

# Load actual consumption files
folder_path = os.path.join('data', 'smard')
file_path1 = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_DE_AT_LU.xlsx')
file_path2 = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_DE_LU.xlsx')
df1 = pd.read_excel(file_path1)
df2 = pd.read_excel(file_path2)
actual_consumption = pd.concat([df1, df2]).reset_index(drop=True)
actual_consumption.to_csv(os.path.join(folder_path, 'actual_consumption.csv'),  index=False)

#Day-ahead prices data
file_path3 = os.path.join(folder_path, 'Day-ahead_prices_201501010000_202401010600_Hour_DE_AT_LU.xlsx')
df3 = pd.read_excel(file_path3)
issues1 = detect_hyphen_values(df3)
df3.to_csv(os.path.join(folder_path, 'day_ahead_prices.csv'),  index=False)

pass 





