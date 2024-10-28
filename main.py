
# Import helper function 
from core import(readStorageDispatchScenario, 
                 readLoadPrice, 
                 runStorageDispatchCases, 
                 runStorageDispatchSensitivitydelta,
                 runStorageDispatchSensitivityShare,
                 runStorageConfiguration,
                 )
from results_analysis import (plotStorageDispatchCases,
                              plotStorageDispatchSensitivitydelta,
                              plotStorageDispatchSensitivityShare,
                              plotStorageConfiguration,
                              plotdataAnalysis
                              )



# read storage dispatch scenarios
SCENARIO_LIST = list(range(1, 30))
SCENARIOS, params = readStorageDispatchScenario(SCENARIO_LIST)

#Read price load, and base_tariff
DF_LOAD, DF_PRICE = readLoadPrice()
base_tariff = float(params['scenario_1']['global']['network']['base_tariff'])

#Data analysis 
#plotdataAnalysis(DF_LOAD, DF_PRICE)

''' 
#Step1: compare storage dispatch for each tarifs design 
print("STEP 1 : STORAGE DISPATCH INCLUDING TARIFF SIGNALS")
#Select scenarois for base cases: 1,2,3,4
scenario_cases = SCENARIOS[:4]
selected_years = ["2019","2020", "2021", "2022", "2023"]
# Run storage dispatch for base cases:
#Plot hourly storage dispatch for base cases
#Plot comparison storage dispatch vs price (base_price+ tariff).
STORAGE_RESULT = runStorageDispatchCases(params, scenario_cases, DF_PRICE, base_tariff, DF_LOAD)
plotStorageDispatchCases(scenario_cases, STORAGE_RESULT, selected_years, params)
'''



'''
print("STEP 2 : SENSITIVITY ANALYSIS FOR STORAGE DISPATCH")  
#Sensitity analysis for delta
scenario_cases = SCENARIOS[4:13]
STORAGE_RESULT = runStorageDispatchSensitivitydelta(params, scenario_cases, DF_PRICE, base_tariff, DF_LOAD)
categories = ['Revenue Market', 'Revenue Tariff', 'Total Revenue']
plotStorageDispatchSensitivitydelta(params, STORAGE_RESULT,categories)
'''

'''
# sensitivity analysis for share 
print("-*- Sensitivity analysis on share")
scenario_cases = SCENARIOS[13:25]
STORAGE_RESULT = runStorageDispatchSensitivityShare(params, scenario_cases, DF_PRICE, base_tariff, DF_LOAD)
plotStorageDispatchSensitivityShare(params, STORAGE_RESULT)
'''



print("STEP 4: EX-ANTE TARIFF VS EX-POST TARIFF")
scenario_cases = SCENARIOS[25:29]
STORAGE_RESULT = runStorageConfiguration(params, scenario_cases, DF_PRICE, base_tariff, DF_LOAD) 
plotStorageConfiguration(scenario_cases, STORAGE_RESULT, params)






''' 
#Plot load vs price
start = int(params['scenario_1']['global']['config']['start']) # start year for horizon simualtion
end = int(params['scenario_1']['global']['config']['end']) # end year for horizon simulation

for year in range(start, end + 1):
    shadow_price = DF_PRICE[DF_PRICE['year'] == year]['Day-ahead Price [EUR/MWh]']
    df_load = DF_LOAD[DF_LOAD['year'] == year]['Day-ahead Total Load Forecast [MW]']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df_load.values, shadow_price.values, label=f'{year}', color='blue', alpha=0.7)

    # Add title and labels
    plt.title(f'Shadow Price vs. Load for Year {year}')
    plt.xlabel('Day-ahead Total Load Forecast [MW]')
    plt.ylabel('Day-ahead Price [EUR/MWh]')
    plt.legend()

    # Show the plot
    plt.show()
    
'''




