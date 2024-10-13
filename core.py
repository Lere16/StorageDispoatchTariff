import os
import settings
import pandas as pd
from storage_dispatch.batterydispatch_for_kWh_ import bat_optimize_

def readStorageDispatchScenario(SCENARIO_LIST):
    # Set scenario path
    INPUT_PATH=os.path.join(os.path.dirname(__file__),"data", "input")
    SCENARIO_FILE = os.path.join(INPUT_PATH, "storage_dispatch_scenarios.csv")

    #read input
    params=settings.read(SCENARIO_FILE)
    SCENARIOS= [list(params.keys())[i-1] for i in SCENARIO_LIST]

    return SCENARIOS, params

def readLoadPrice():
    # Set scenario path
    DATA_PATH=os.path.join(os.path.dirname(__file__),"data", "input")
    LOAD_FILE = os.path.join(DATA_PATH, "compiled_load.csv")
    LOAD_PRICE_FILE = os.path.join(DATA_PATH, "compiled_price.csv")
    
    return pd.read_csv(LOAD_FILE), pd.read_csv(LOAD_PRICE_FILE)
    



def runStorageDispatchCases(params, scenario_cases, SHADOW_PRICE, base_tariff, DF_LOAD):
    
    start = int(params['scenario_1']['global']['config']['start']) # start year for horizon simualtion
    end = int(params['scenario_1']['global']['config']['end']) # end year for horizon simulation
    VOLL = float(params['scenario_1']['global']['network']['VOLL'])
    delta = float(params['scenario_1']['global']['tariff']['delta'])
    size = int(params['scenario_1']['global']['parameter']['size'])
    
    STORAGE_RESULT={}
    
     
    for scenario in scenario_cases:
        print(scenario)
        df_combined = pd.DataFrame()
        for year in range(start, end + 1):
            print(year)
            shadow_price = SHADOW_PRICE[year]
            df_load = DF_LOAD[year]
            storage_dispatch = bat_optimize_(params, shadow_price, df_load, scenario, size, base_tariff, VOLL, delta)
            current_data = storage_dispatch.info["data"]
            current_data['Pc'] = current_data['Pc'] * (-1)
            current_data['year'] = year
            df_combined = pd.concat([df_combined, current_data], ignore_index=True)
            
        
        df_combined['price'] = df_combined["base_price"] + df_combined["tariff"]
        df_combined['dispatch'] = df_combined["Pd"] + df_combined["Pc"]
        
        STORAGE_RESULT[scenario] = df_combined
        df_combined.to_csv(os.path.join('results/CSV', f"storage_result_{scenario}.csv"), index=False)
    
            
    STORAGE_RESULT_TEMP=STORAGE_RESULT.copy()
    recovered_cost_tariff = []
    recovered_cost_price = []
    for scenario, data in STORAGE_RESULT_TEMP.items():
        
        if scenario == 'scenario_1':
            continue
        
        df = data
        df['net_load_tariff'] = df['net_load'] * df['tariff']
        net_load_tariff_sum = df['net_load_tariff'].sum()
        recovered_cost_tariff.append({'scenario': scenario, 'recovered_cost': net_load_tariff_sum})
        
        df['net_load_price'] = df['net_load'] * df['price']
        net_load_price_sum = df['net_load_price'].sum()
        recovered_cost_price.append({'scenario': scenario, 'recovered_cost': net_load_price_sum})
        
    results_tariff = pd.DataFrame(recovered_cost_tariff)
    results_price = pd.DataFrame(recovered_cost_price)
    results_tariff.to_csv(os.path.join('results/CSV', f"recovered_costs_by_tariff.csv"), index=False)
    results_price.to_csv(os.path.join('results/CSV', f"recovered_costs_by_price.csv"), index=False)

    return STORAGE_RESULT
