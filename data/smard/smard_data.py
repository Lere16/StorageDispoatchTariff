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
# DE/LU
folder_path = os.path.join('data', 'smard')

def load_germany():
    # Load actual consumption files
    folder_path = os.path.join('data', 'smard')
    file_path1 = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_DE_AT_LU.xlsx')
    file_path2 = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_DE_LU.xlsx')
    df1 = pd.read_excel(file_path1)
    df2 = pd.read_excel(file_path2)
    actual_consumption = pd.concat([df1, df2]).reset_index(drop=True)
    actual_consumption['Start date'] = pd.to_datetime(actual_consumption['Start date'], format='%b %d, %Y %I:%M %p')
    actual_consumption['End date'] = pd.to_datetime(actual_consumption['End date'], format='%b %d, %Y %I:%M %p')
    actual_consumption['Start date'] = actual_consumption['Start date'].dt.strftime('%d/%m/%Y %H:%M')
    actual_consumption['End date'] = actual_consumption['End date'].dt.strftime('%d/%m/%Y %H:%M')
    actual_consumption.to_csv(os.path.join(folder_path, 'actual_consumption.csv'),  index=False)
    
    return actual_consumption 

#Day-ahead prices data
def prices_germany():
    file_path3 = os.path.join(folder_path, 'Day-ahead_prices_201501010000_202401010600_Hour_DE_AT_LU.xlsx')
    df3 = pd.read_excel(file_path3)
    issues1 = detect_hyphen_values(df3)
    df3['Start date'] = pd.to_datetime(df3['Start date'], format='%b %d, %Y %I:%M %p')
    df3['End date'] = pd.to_datetime(df3['End date'], format='%b %d, %Y %I:%M %p')
    df3['Start date'] = df3['Start date'].dt.strftime('%d/%m/%Y %H:%M')
    df3['End date'] = df3['End date'].dt.strftime('%d/%m/%Y %H:%M')
    df3.to_csv(os.path.join(folder_path, 'day_ahead_prices.csv'),  index=False)
    df3.to_csv(os.path.join(folder_path, 'day_ahead_prices_50Hertz.csv'),  index=False)
    df3.to_csv(os.path.join(folder_path, 'day_ahead_prices_Amprion.csv'),  index=False)
    df3.to_csv(os.path.join(folder_path, 'day_ahead_prices_TenneT.csv'),  index=False)
    df3.to_csv(os.path.join(folder_path, 'day_ahead_prices_TransnetBW.csv'),  index=False)
    
    return df3, issues1

def load_price_germany():
    
    return None 

def load_50Hertz():
    #load
    path_cons_50Hertz = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_50Hertz.xlsx')
    cons_50Hertz = pd.read_excel(path_cons_50Hertz)
    issues_50Hertz = detect_hyphen_values(cons_50Hertz)
    cons_50Hertz['Start date'] = pd.to_datetime(cons_50Hertz['Start date'], format='%b %d, %Y %I:%M %p')
    cons_50Hertz['End date'] = pd.to_datetime(cons_50Hertz['End date'], format='%b %d, %Y %I:%M %p')
    cons_50Hertz['Start date'] = cons_50Hertz['Start date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_50Hertz['End date'] = cons_50Hertz['End date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_50Hertz.to_csv(os.path.join(folder_path, 'actual_consumption_50Hertz.csv'),  index=False)
    return cons_50Hertz, issues_50Hertz

def load_Amprion():
    #Amprion
    path_cons_Amprion = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_Amprion.xlsx')
    cons_Amprion = pd.read_excel(path_cons_Amprion)
    issues_Amprion = detect_hyphen_values(cons_Amprion)
    cons_Amprion['Start date'] = pd.to_datetime(cons_Amprion['Start date'], format='%b %d, %Y %I:%M %p')
    cons_Amprion['End date'] = pd.to_datetime(cons_Amprion['End date'], format='%b %d, %Y %I:%M %p')
    cons_Amprion['Start date'] = cons_Amprion['Start date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_Amprion['End date'] = cons_Amprion['End date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_Amprion.to_csv(os.path.join(folder_path, 'actual_consumption_Amprion.csv'),  index=False)
    return cons_Amprion, issues_Amprion

def load_TenneT():
    #Tennet
    path_cons_TenneT = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_TenneT.xlsx')
    cons_TenneT = pd.read_excel(path_cons_TenneT)
    issues_TenneT = detect_hyphen_values(cons_TenneT)
    cons_TenneT['Start date'] = pd.to_datetime(cons_TenneT['Start date'], format='%b %d, %Y %I:%M %p')
    cons_TenneT['End date'] = pd.to_datetime(cons_TenneT['End date'], format='%b %d, %Y %I:%M %p')
    cons_TenneT['Start date'] = cons_TenneT['Start date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_TenneT['End date'] = cons_TenneT['End date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_TenneT.to_csv(os.path.join(folder_path, 'actual_consumption_Tennet.csv'),  index=False)


    return issues_TenneT, cons_TenneT

#TransnetBW
def load_TransnetBW():
    path_cons_TransnetBW = os.path.join(folder_path, 'Actual_consumption_201501010000_202401010600_Hour_TransnetBW.xlsx')
    cons_TransnetBW = pd.read_excel(path_cons_TransnetBW)
    issues_TransnetBW = detect_hyphen_values(cons_TransnetBW)
    cons_TransnetBW['Start date'] = pd.to_datetime(cons_TransnetBW['Start date'], format='%b %d, %Y %I:%M %p')
    cons_TransnetBW['End date'] = pd.to_datetime(cons_TransnetBW['End date'], format='%b %d, %Y %I:%M %p')
    cons_TransnetBW['Start date'] = cons_TransnetBW['Start date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_TransnetBW['End date'] = cons_TransnetBW['End date'].dt.strftime('%d/%m/%Y %H:%M')
    cons_TransnetBW.to_csv(os.path.join(folder_path, 'actual_consumption_TransnetBW.csv'),  index=False)

    return  issues_TransnetBW, cons_TransnetBW
    

#cons_50Hertz, issues_50Hertz = load_50Hertz()

prices, issues = prices_germany()



pass 





