
from core import*

# read storage dispatch scenarios
SCENARIO_LIST = list(range(1, 30))
SCENARIOS, params = readStorageDispatchScenario(SCENARIO_LIST)

#Read price load, and base_tariff
DF_LOAD, DF_PRICE = readLoadPrice()
base_tariff = float(params['scenario_1']['global']['network']['base_tariff'])

#Step1: compare storage dispatch for each tarifs design 
print("STEP 1 : STORAGE DISPATCH INCLUDING TARIFF SIGNALS")
#Select scenarois for base cases: 1,2,3,4
scenario_cases = SCENARIOS[:4]
selected_years = ["2019","2020", "2021", "2022", "2023"]
# Run storage dispatch for base cases:
#Plot hourly storage dispatch for base cases
#Plot comparison storage dispatch vs price (base_price+ tariff).
STORAGE_RESULT = runStorageDispatchCases(params, scenario_cases, DF_PRICE, base_tariff, DF_LOAD)

#plotStorageDispatchCases(scenario_cases, STORAGE_RESULT, selected_years, params)


