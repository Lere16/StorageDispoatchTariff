import os

import pandas as pd
import numpy as np
from matplotlib import rcParams
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'firefox'
from plotly.offline import plot
import os
import altair as alt
from datetime import datetime, timedelta
from altair_saver import save
from matplotlib.colors import to_hex
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import statsmodels.api as sm
import plotly.graph_objects as go
from matplotlib.ticker import ScalarFormatter




# MAIN PLOTING FUNCTION 
def plotStorageDispatchCases(scenario_cases, STORAGE_RESULT, selected_years, params):
    
    year_plot= int(params[scenario_cases[0]]['global']['plot']['year_plot'])
    start_hour=int(params[scenario_cases[0]]['global']['plot']['start_hour'])
    end_hour= int(params[scenario_cases[0]]['global']['plot']['end_hour'])
    
    #make directory for plots
    
    output_dir = 'results/plots/storage_dispatch'
    os.makedirs(output_dir, exist_ok=True)
    
    #Plot hourly storage dipatch for each scenario as sngle plot
    
    for scenario in scenario_cases:
        df = STORAGE_RESULT[scenario].loc[(STORAGE_RESULT[scenario]['year'] == year_plot) & (STORAGE_RESULT[scenario]['hour'].between(start_hour, end_hour))]; df = df.set_index('hour')
        # Plot Storage dispatch
        labels_storage = ['charge', 'discharge', 'tariff_level']
        colors_storage= ['hotpink', 'darkcyan', 'black']
        fig_storagedispatch, ax1= hourlyStorageDispatch(labels_storage, colors_storage, df_area=df[['Pc', 'Pd']], df_line=df[['tariff']], sto_level=True, legend=True)
        fig_storagedispatch.savefig(os.path.join(output_dir, f'storage_dispatch_{scenario}.png'), dpi=350)
    
    
    #for all scenarios in one 
    num_scenarios = len(scenario_cases)
    labels_storage = ['charge', 'discharge', 'tariff_level']
    colors_storage = ['hotpink', 'darkcyan', 'black']

    fig, axes = plt.subplots(num_scenarios, 1, figsize=(15, 4 * num_scenarios), sharex=True, sharey=True)
    scenarios_labels = {scenario_cases[0]: params[scenario_cases[0]]['global']['tariff']['shape'],
                        scenario_cases[1]: params[scenario_cases[1]]['global']['tariff']['shape'],
                        scenario_cases[2]: params[scenario_cases[2]]['global']['tariff']['shape'],
                        scenario_cases[3]: params[scenario_cases[3]]['global']['tariff']['shape'],
                        }
    
    for i, scenario in enumerate(scenario_cases):
        df = STORAGE_RESULT[scenario].loc[(STORAGE_RESULT[scenario]['year'] == year_plot) & (STORAGE_RESULT[scenario]['hour'].between(start_hour, end_hour))]
        df = df.set_index('hour')

        ax = axes[i] if num_scenarios > 1 else axes  
        hourlyStorageDispatch_2(labels_storage, colors_storage, df_area=df[['Pc', 'Pd']], df_line=df[['tariff']], sto_level=True, legend=False, ax1=ax)

        ax.set_title(f'{scenarios_labels[scenario]}')
    

    axes[-1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=num_scenarios*2, fontsize=12, frameon=False)

    plt.savefig(os.path.join(output_dir, f'HourlystorageDispatchCombine.png'), dpi=350)    

    
    #Plot comparison storage dispatch vs price
    dispatch_price ={}
    
    for scenario in scenario_cases:
        df1 = STORAGE_RESULT[scenario]
        dispatch = df1[['Pc', 'Pd', 'price']] 
        dispatch_price[scenario] = dispatch
    # First option: Charging and discgarging are separated
    fig_dispatchprice_1= plotStorageDispatchPrice(dispatch_price)
    fig_dispatchprice_1.savefig(os.path.join(output_dir, f'storage_dispatch_price_comparison_{year_plot}.png'), dpi=350) 
    # second option: Charging and discgarging are combined
    fig_dispatchprice_2= plotStorageDispatchPrice_2(dispatch_price)
    fig_dispatchprice_2.savefig(os.path.join(output_dir, f'storage_dispatch_price_comparison_2_{year_plot}.png'), dpi=350)

    
    
    #Tariff signal comparison
    tariff_signals = {}
    
    for scenario in scenario_cases[-3:]:
        df2 = STORAGE_RESULT[scenario].loc[(STORAGE_RESULT[scenario]['year'] == year_plot) & (STORAGE_RESULT[scenario]['hour'].between(start_hour, end_hour))]
        load_tariff = df2[['hour','tariff', 'net_load']] 
        tariff_signals[scenario] = load_tariff
    
    fig_tariffsignal= plotTariffSignals(tariff_signals)
    fig_tariffsignal.savefig(os.path.join(output_dir, f'tariff_signals_comparison_{year_plot}.png'), dpi=300)

    
    netloadTariff={}
    
    for scenario in scenario_cases[-3:]:
        df3 = STORAGE_RESULT[scenario].loc[(STORAGE_RESULT[scenario]['year'] == year_plot)]
        netloadTariff[scenario]= df3
    fig_tariff_netload = plotNetloadtariff(netloadTariff)
    fig_tariff_netload.savefig(os.path.join(output_dir, f'netload_tariff.png'), dpi=300)

    
    #Plot netload vs revenue
    combined_df1={}
    combined_df2={}
    combined_df ={}
    selected_df={}
    
    #for scenario, df in STORAGE_RESULT.items():
        
    # Concatenate DataFrames for each scenario
    combined_df1= pd.concat([df.assign(scenario=scenario) for scenario, df in STORAGE_RESULT.items()], ignore_index=True)
    # Convert 'year' column to string
    combined_df1['year'] = combined_df1['year'].astype(str)
    # Calculate profit
    combined_df1['profit'] = combined_df1['dispatch'] * combined_df1['price'] # without annual cap_cost and annual OM 
    # Map scenario names to selected tariffs
    #selected_tariff = ["flat", "proportional", "piecewise"]
    selected_tariff = [params[scenario_cases[1]]['global']['tariff']['shape'], 
                        params[scenario_cases[2]]['global']['tariff']['shape'], 
                        params[scenario_cases[3]]['global']['tariff']['shape']]
    scenario_tariff_mapping = {}
    for i, scenario in enumerate(scenario_cases[1:]):
        scenario_tariff_mapping[scenario] = selected_tariff[i]
    combined_df1['scenario'] = combined_df1['scenario'].replace(scenario_tariff_mapping)
    # Plot netload revenue line
    fig_profit_netload = plotNetloadRevenue_line(pd.DataFrame(combined_df1))
    # Write HTML file
    fig_profit_netload.write_html(os.path.join(output_dir, f'netload_profit.html'))
    
    #STOP OK
    # Only revenue to avoid negative part
    
    combined_df2= pd.concat([df.assign(scenario=scenario) for scenario, df in STORAGE_RESULT.items()], ignore_index=True)
    combined_df2['year'] = combined_df2['year'].astype(str)
    combined_df2['revenue'] = combined_df2['Pd']*combined_df2['price']
    #selected_tariff = ["without tarif", "flat", "proportional", "piecewise"]
    selected_tariff = [ params[scenario_cases[0]]['global']['tariff']['shape'],
                        params[scenario_cases[1]]['global']['tariff']['shape'], 
                        params[scenario_cases[2]]['global']['tariff']['shape'], 
                        params[scenario_cases[3]]['global']['tariff']['shape']]
    scenario_tariff_mapping = {}
    for i, scenario in enumerate(scenario_cases):
        scenario_tariff_mapping[scenario] = selected_tariff[i]
    combined_df2['scenario'] = combined_df2['scenario'].replace(scenario_tariff_mapping)
    fig_revenue_netload = plotNetloadRevenue_line_2(pd.DataFrame(combined_df2))
    fig_revenue_netload.write_html(os.path.join(output_dir, f'netload_revenue.html'))
    
    
    
    #Revenue vs tariff 
    fig_revenue_tariff= plotTariffRevenue_line(pd.DataFrame(combined_df2))
    fig_revenue_tariff.write_html(os.path.join(output_dir, f'Tariff_revenue.html'))



    # Plot Storage dispatch vs price over years 
    selected_scenarios = scenario_cases[-3:]
    combined_df = pd.concat([df.assign(scenario=scenario) for scenario, df in STORAGE_RESULT.items()], ignore_index=True)
    combined_df['year'] = combined_df['year'].astype(str)
    selected_df = combined_df[(combined_df['scenario'].isin(selected_scenarios)) & (combined_df['year'].isin(selected_years[-2:]))]
    
    scenario_mapping = {scenario_cases[0]: params[scenario_cases[0]]['global']['tariff']['shape'], 
                        scenario_cases[1]: params[scenario_cases[1]]['global']['tariff']['shape'], 
                        scenario_cases[2]: params[scenario_cases[2]]['global']['tariff']['shape'], 
                        scenario_cases[3]: params[scenario_cases[3]]['global']['tariff']['shape']}
    selected_df['scenario'] = selected_df['scenario'].replace(scenario_mapping)
    fig_dispatch_year = plotStorageDispatchYears(selected_years[-2:], selected_scenarios, pd.DataFrame(selected_df))
    fig_dispatch_year.write_html(os.path.join(output_dir, f'storage_dispatch_tariff_comparison.html'))

    
    #Plot storage dispatch volume
    selected_scenarios = scenario_cases[-3:]
    combined_df = pd.concat([df.assign(scenario=scenario) for scenario, df in STORAGE_RESULT.items()], ignore_index=True)
    combined_df['year'] = combined_df['year'].astype(str)
    selected_df = combined_df[(combined_df['scenario'].isin(selected_scenarios)) & (combined_df['year'].isin(selected_years[-3:]))]
    scenario_mapping = {scenario_cases[0]: params[scenario_cases[0]]['global']['tariff']['shape'], 
                        scenario_cases[1]: params[scenario_cases[1]]['global']['tariff']['shape'], 
                        scenario_cases[2]: params[scenario_cases[2]]['global']['tariff']['shape'], 
                        scenario_cases[3]: params[scenario_cases[3]]['global']['tariff']['shape']}
    selected_df['scenario'] = selected_df['scenario'].replace(scenario_mapping)
    fig_dispatch_year_2 = plotStorageDispatchYears_2(pd.DataFrame(selected_df))
    fig_dispatch_year_2.write_html(os.path.join(output_dir, f'storage_dispatch_tariff_comparison_volume.html'))

    # Plot volume amount for all years
    selected_scenarios = scenario_cases[-4:]
    combined_df = pd.concat([df.assign(scenario=scenario) for scenario, df in STORAGE_RESULT.items()], ignore_index=True)
    combined_df['year'] = combined_df['year'].astype(str)
    selected_df = combined_df[(combined_df['scenario'].isin(selected_scenarios)) & (combined_df['year'].isin(selected_years[-3:]))]
    scenario_mapping = {scenario_cases[0]: params[scenario_cases[0]]['global']['tariff']['shape'], 
                        scenario_cases[1]: params[scenario_cases[1]]['global']['tariff']['shape'], 
                        scenario_cases[2]: params[scenario_cases[2]]['global']['tariff']['shape'], 
                        scenario_cases[3]: params[scenario_cases[3]]['global']['tariff']['shape']}
    selected_df['scenario'] = selected_df['scenario'].replace(scenario_mapping)
    fig_dispatch_vol=plotDispatchVolume(pd.DataFrame(selected_df))
    fig_dispatch_vol.write_html(os.path.join(output_dir, f'storage_dispatch_volume.html'))
        
    
    # compare revenue for all scenarios:    
    plot_revenue_comparison(STORAGE_RESULT, params, output_dir)
    plot_tariff_revenue_comparison(STORAGE_RESULT, params, output_dir)
    return None 



#STEP2 

def plotStorageDispatchSensitivitydelta(params, STORAGE_RESULT, categories):
    
    output_dir = 'results/plots/storage_dispatch'
    os.makedirs(output_dir, exist_ok=True)
    
    #average revenue for sensitivity on delta 
    plot_storage_revenues(STORAGE_RESULT, params, categories, output_dir)
    #stacked revenues for snesitivity on delta 
    plot_stacked_revenues(STORAGE_RESULT, params, output_dir)
    # Stacked market and Tariff revenue only
    plot_stacked_revenues_2(STORAGE_RESULT, params, output_dir)
    # stacked bars with percentage
    plot_stacked_revenues_3(STORAGE_RESULT, params, output_dir)

    
    return None
    

def plotStorageDispatchSensitivityShare(params, STORAGE_RESULT):
    
    output_dir = 'results/plots/storage_dispatch'
    os.makedirs(output_dir, exist_ok=True)
    plot_stacked_revenues_by_shape(STORAGE_RESULT, params, output_dir)
    plot_stacked_revenues_by_shape_horizontal(STORAGE_RESULT, params, output_dir)
    plot_stacked_revenues_by_shape_vertical(STORAGE_RESULT, params, output_dir)

    return None 

    







# ..................................................................HELPER FUNCTION 


# hourly storage dispatch in different file 
def hourlyStorageDispatch(labels, colors, sto_level=False, df_area=None, df_line=None, legend=True, legend_position='upper center', legend_col_no=8, figsize=(15,6), bottom_fix=0.3, fontsize=12, ticksize=12, legfontsize=12 ):
    
    fig, ax1 = plt.subplots(figsize=figsize)
    ax2=ax1.twinx()
    # Stacked area plot
    x = range(int(df_area.index[0]), int(df_area.index[-1])+1)
    df_area_neg, df_area_pos = df_area.clip(upper=0), df_area.clip(lower=0)
    y_pos = [df_area_pos[c].tolist() for c in df_area_pos]
    y_neg = [df_area_neg[c].tolist() for c in df_area_neg]
    area1 = ax1.stackplot( x, y_pos, labels=labels, colors=colors, step='mid')
    area2 = ax1.stackplot( x, y_neg, colors=colors, step='mid')
    if sto_level:
        # line plot1
        line1 = ax2.plot(df_line, color='#434566', linestyle='-.', label='tariff level')
    
    if legend: 
        figs= area1+area2
        if sto_level:
            figs=area1 + area2 + line1 
        labels_all=[f.get_label() for f in figs]
        leg = ax1.legend(figs, labels_all, loc=legend_position, bbox_to_anchor=(0.5, -0.25), ncol=legend_col_no, fontsize=legfontsize, frameon=False)

    # properties
    ax1.set_xlabel('hour', fontsize=fontsize) 
    ax1.set_ylabel('MW', fontsize=fontsize)
    if sto_level:
        ax2.set_ylabel('EUR/MWh', fontsize=fontsize)
    ax1.tick_params(axis='both', which='major', labelsize=ticksize)
    ax2.tick_params(axis='y', which='major', labelsize=ticksize)
    
    plt.margins(x=0)
    plt.tight_layout()
    plt.subplots_adjust(bottom=bottom_fix, top=0.98, left=0.05, right=0.95)
    
    return fig, ax1


#hourly storage dispatch in a single file 
def hourlyStorageDispatch_2(labels, colors, sto_level=False, df_area=None, df_line=None, legend=True, legend_position='upper center', legend_col_no=8, figsize=(15.2,5.6), bottom_fix=0.1, fontsize=12, ticksize=12, legfontsize=12, ax1=None):
    if ax1 is None:
        fig, ax1 = plt.subplots(figsize=figsize)
        ax2 = ax1.twinx()
    else:
        ax2 = ax1.twinx()
    
    x = range(int(df_area.index[0]), int(df_area.index[-1]) + 1)
    df_area_neg, df_area_pos = df_area.clip(upper=0), df_area.clip(lower=0)
    y_pos = [df_area_pos[c].tolist() for c in df_area_pos]
    y_neg = [df_area_neg[c].tolist() for c in df_area_neg]
    area1 = ax1.stackplot(x, y_pos, labels=labels, colors=colors, step='mid')
    area2 = ax1.stackplot(x, y_neg, colors=colors, step='mid')
    if sto_level:
        line1 = ax2.plot(df_line, color='#434566', linestyle='-.', label='tariff level')
    
    if legend:
        figs = area1 + area2
        if sto_level:
            figs = area1 + area2 + line1 
        labels_all = [f.get_label() for f in figs]
        leg = ax1.legend(figs, labels_all, loc=legend_position, bbox_to_anchor=(0.5, -0.25), ncol=legend_col_no, fontsize=legfontsize, frameon=False)

    ax1.set_xlabel('hours', fontsize=fontsize) 
    ax1.set_ylabel('Power [MW]', fontsize=fontsize)
    if sto_level:
        ax2.set_ylabel('Tariff [EUR/MWh]', fontsize=fontsize)
    ax1.tick_params(axis='both', which='major', labelsize=ticksize)
    ax2.tick_params(axis='y', which='major', labelsize=ticksize)
    
    plt.margins(x=0)
    plt.tight_layout()
    plt.subplots_adjust(bottom= bottom_fix, top=0.98, left=0.05, right=0.95)
    
    if ax1 is None:
        return fig, ax1
    else:
        return ax1

def plotStorageDispatchPrice(data): 
    
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    fig.suptitle(' Storage dispatch vs prices')
    scenarios  = list(data.keys())
    
    tariff_types = ['without tariff', 'flat tariff', 'proportional tariff', 'piecewise tariff']

    for i, scenario in enumerate(scenarios):
        
        row = i // 2
        col = i % 2
        ax = axs[row, col]
        
        ax.scatter(data[scenario]['price'], data[scenario]['Pc'], label='Pc', color='blue', s=22)
        ax.scatter(data[scenario]['price'], data[scenario]['Pd'], label='Pd', color='red', s=22)
        
        ax.set_title(f'{tariff_types[i]}')
        ax.set_xlabel('Price')
        ax.set_ylabel('Pd/Pc')
        ax.legend()
        ax.tick_params(axis='both', labelsize=7)
        
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    return plt.gcf()


def plotStorageDispatchPrice_2(data): 
    
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    fig.suptitle(' Storage dispatch vs prices')
    scenarios  = list(data.keys())
    
    tariff_types = ['without tariff', 'flat tariff', 'proportional tariff', 'piecewise tariff']

    for i, scenario in enumerate(scenarios):
        
        row = i // 2
        col = i % 2
        ax = axs[row, col]
        
        ax.scatter(data[scenario]['price'], data[scenario]['Pc'] + data[scenario]['Pd'] , label='Pd-Pc', color='blue')

        ax.set_title(f'{tariff_types[i]}')
        ax.set_xlabel('Price (EUR/MWh)')
        ax.set_ylabel('Pd-Pc (MW)')
        ax.legend()
        ax.tick_params(axis='both', labelsize=7)
        
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    return plt.gcf()


def plotTariffSignals(tariff_signals):
    num_scenarios = len(tariff_signals)
    scenario_labels = ["flat", "proportional", "piecewise"]

    # Plot setup
    fig, axes = plt.subplots(1, num_scenarios, figsize=(3.5* num_scenarios, 3.5))

    for i, (scenario_name, scenario_data) in enumerate(tariff_signals.items()):
        ax = axes[i] if num_scenarios > 1 else axes  # Handle single scenario case

        # Extract data
        tariff = scenario_data['tariff']
        net_load = scenario_data['net_load']
        hour = scenario_data['hour']
        ax.set_title(f'{scenario_labels[i]}')
        
        label = scenario_labels[i]

        # Plot tariff on the first y-axis
        ax.plot(hour, tariff, label=f'{label}', color='blue', linestyle='-', marker='o', markersize=2)
        ax.set_xlabel('Hours')
        ax.set_ylabel('Tariff (EUR/MWh)', color='blue')
        ax.tick_params('y', colors='blue')
        #ax.legend(loc='upper left')

        # Create a second y-axis that shares the same x-axis
        ax2 = ax.twinx()

        # Plot net_load on the second y-axis
        ax2.plot(hour, net_load, label='Net Load', color='brown')
        ax2.set_ylabel('Net Load (MW)', color='brown')
        ax2.tick_params('y', colors='brown')
        #ax2.legend(loc='upper right')
        
        # Set scalar formatter for y-axis
        #ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

        ax.tick_params(axis='both', labelsize=8)

    plt.tight_layout(rect=[0, 0, 1, 1])
    return plt.gcf()


def plotNetloadtariff(data):
    fig, axs = plt.subplots(1, 3, figsize=(11, 4))
    
    tariff_types = ['flat', 'proportional', 'piecewise']

    for i, (scenario, df_scenario) in enumerate(data.items()):
        ax = axs[i]

        ax.scatter(df_scenario['net_load'], df_scenario['tariff'], s=12, alpha=.9)
        ax.set_title(f'{tariff_types[i]}')
        ax.set_xlabel('Net Load (MW)')
        ax.set_ylabel('Tariff (EUR/MWh)')

        # Masquer les bords supérieur et droit du subplot
        ax.spines[['top', 'right']].set_visible(False)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))

    # Ajuster la disposition pour éviter les chevauchements
    plt.tight_layout()

    return plt.gcf()


def plotNetloadRevenue_line(df):
    fig = px.line(df, x='net_load', y='profit', color='year', facet_col="scenario", labels={'net_load': 'Net load (MW)', 'profit': 'Profit (EUR/h)'})
    return fig


def plotNetloadRevenue_line_2(df):
    last_three_years = sorted(df['year'].unique())[-4:]
    filtered_df = df[df['year'].isin(last_three_years)]
    fig = px.line(filtered_df, x='net_load', y='revenue', color='year', facet_col="scenario", labels={'net_load': 'Net load (MW)', 'revenue': 'Revenue (EUR/h)'}, template="simple_white", width=960, height=600)
    return fig

def plotTariffRevenue_line(df):
    fig = px.line(df, x='tariff', y='revenue', color='year', facet_col="scenario", labels={'tariff': 'Tariff (EUR/MWh)', 'revenue': 'Revenue (EUR/h)'}, template="simple_white", width=960, height=600)
    return fig

def plotStorageDispatchYears(years, scenarios,df):
    fig = px.scatter(df, x='price', y='dispatch', facet_row="year", facet_col='scenario', facet_col_wrap=4, labels={'price': 'Price (EUR/MWh)', 'dispatch': 'Dispatch (MW)'})    
    return fig


def plotStorageDispatchYears_2(df):
    df['Pc'] = df['Pc'].abs()
    # Create scatter plot for Pd
    fig = px.scatter(df, x="price", y="dispatch", size="Pd", facet_row="year", facet_col="scenario", 
                     hover_name="year", log_x=False, size_max=60, width=900, height=800, labels={'price': 'Price (EUR/MWh)', 'dispatch': 'Energy (MWh)'}, template="simple_white")
    # Add trace for Pc with a different color
    num_traces = len(fig.data)
    for i in range(num_traces):
        fig.add_trace(px.scatter(df, x="price", y="dispatch", size="Pc", facet_row="year", facet_col="scenario", 
                             hover_name="year", log_x=False, size_max=60).update_traces(marker=dict(color='brown')).data[i])
    return fig


def plotDispatchVolume(df):
    df['Pc'] = df['Pc'].abs()
    
    grouped_df = df.groupby(["scenario", "year"]).agg({"Pd": "sum", "Pc": "sum"}).reset_index()
    grouped_df = grouped_df.rename(columns={"Pd": "discharged"})
    grouped_df = grouped_df.rename(columns={"Pc": "charged"})
    melted_df = pd.melt(grouped_df, id_vars=["scenario", "year"], value_vars=["discharged", "charged"], var_name="type", value_name="energy")
    
    fig = px.bar(melted_df, x="year", y="energy", color="year", facet_col="scenario", facet_row="type",
             labels={"energy": "Total Energy (MWh)", "year": "Year", "scenario": "Scenario", "type": "Type",},
             height=900, width=1080, template="simple_white")

    # Ajouter les valeurs sur les barres
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    
    
    return fig



def plot_revenue_comparison(STORAGE_RESULT, params, output_dir):
    # Obtenir toutes les formes uniques
    shapes = sorted(set(params[scenario]['global']['tariff']['shape'] for scenario in STORAGE_RESULT.keys()))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Couleurs pour Market Revenue, Tariff Revenue, Total Revenue
    hatches = ['-', '+', 'x', 'o', 'O', '.', '*']  # Différents types de hachures
    bar_width = 0.2

    fig, ax = plt.subplots(figsize=(10, 8))

    shape_idx = 0
    shapes_labels = []  # Pour stocker les étiquettes des formes
    num_scenarios_per_shape = []  # Pour stocker le nombre de scénarios par forme

    for shape in shapes:
        average_market_revenues = []
        average_tariff_revenues = []
        average_total_revenues = []

        for scenario, df_delta in STORAGE_RESULT.items():
            if params[scenario]['global']['tariff']['shape'] == shape:
                # Calculer les revenus
                df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']
                df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']

                # Calculer les revenus annuels moyens
                annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().mean()
                annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().mean()
                total_revenue = annual_market_revenue + annual_tariff_revenue

                # Stocker les valeurs
                average_market_revenues.append(annual_market_revenue)
                average_tariff_revenues.append(annual_tariff_revenue)
                average_total_revenues.append(total_revenue)

        # Convertir les listes en arrays numpy
        average_market_revenues = np.array(average_market_revenues)
        average_tariff_revenues = np.array(average_tariff_revenues)
        average_total_revenues = np.array(average_total_revenues)

        # Indices pour les barres
        index = np.arange(len(average_market_revenues))

        # Décalage pour les groupes de barres
        offset = shape_idx * bar_width * 4

        # Tracer les barres
        ax.bar(index + offset, average_market_revenues, bar_width, color=colors[0], edgecolor='black', hatch=hatches[shape_idx % len(hatches)], label='Market Revenue' if shape_idx == 0 else "")
        ax.bar(index + offset + bar_width, average_tariff_revenues, bar_width, color=colors[1], edgecolor='black', hatch=hatches[shape_idx % len(hatches)], label='Tariff Revenue' if shape_idx == 0 else "")
        ax.bar(index + offset + 2 * bar_width, average_total_revenues, bar_width, color=colors[2], edgecolor='black', hatch=hatches[shape_idx % len(hatches)], label='Total Revenue' if shape_idx == 0 else "")

        # Ajouter les labels pour les formes
        shapes_labels.extend([f'{shape}'])
        num_scenarios_per_shape.append(len(average_market_revenues))
        shape_idx += 1

    # Ajuster les positions des ticks et leurs labels
    total_bars = sum(num_scenarios_per_shape)
    ticks_positions = np.arange(total_bars) * bar_width * 4 + bar_width
    ax.set_xticks(ticks_positions)
    ax.set_xticklabels(shapes_labels, rotation=0, ha='right', fontsize=10)  # Augmenter la taille des labels des ticks

    ax.set_xlabel('Shapes', fontsize=10)  # Augmenter la taille de l'étiquette de l'axe x
    ax.set_ylabel('Average Revenue (EUR/y)', fontsize=10)  # Augmenter la taille de l'étiquette de l'axe y
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)  # Augmenter la taille de la légende

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "revenue_comparison.png"), dpi=350)
    return None 


def plot_tariff_revenue_comparison(STORAGE_RESULT, params, output_dir):
    
    # Obtenir toutes les formes uniques sauf "without_tariff"
    shapes = sorted(set(params[scenario]['global']['tariff']['shape'] for scenario in STORAGE_RESULT.keys()))
    shapes = [shape for shape in shapes if shape != "without_tariff"]  # Exclure "without_tariff"
    colors = ['#ff7f0e']  # Couleur pour Tariff Revenue
    hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']  # Différents types de hachures
    bar_width = 0.2

    # Définir le nombre de sous-graphiques
    num_shapes = len(shapes)
    fig, axes = plt.subplots(1, num_shapes, figsize=(4 * num_shapes, 5), sharey=True)

    # Assurer que axes est toujours une liste même si n == 1
    if num_shapes == 1:
        axes = [axes]

    for shape_idx, shape in enumerate(shapes):
        ax = axes[shape_idx]
        annual_tariff_revenues = []
        years = []

        for scenario, df_delta in STORAGE_RESULT.items():
            if params[scenario]['global']['tariff']['shape'] == shape:
                # Calculer les revenus tarifaires annuels
                df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
                annual_revenue = df_delta.groupby('year')['revenue_tariff'].sum()

                # Ajouter les revenus et les années
                annual_tariff_revenues.extend(annual_revenue)
                years.extend(annual_revenue.index)

        # Convertir les listes en arrays numpy
        annual_tariff_revenues = np.array(annual_tariff_revenues)
        years = np.array(years)

        # Indices pour les barres
        index = np.arange(len(years))

        # Tracer les barres
        ax.bar(index, annual_tariff_revenues, bar_width, color=colors[0], edgecolor='black', hatch=hatches[shape_idx % len(hatches)], label='Tariff Revenue')

        # Ajouter les labels pour les années
        ax.set_xticks(index)
        ax.set_xticklabels(years, rotation=90, ha='right', fontsize=12)  # Augmenter la taille des labels des ticks
        ax.set_title(f'{shape}', fontsize=14)  # Augmenter la taille du titre

    fig.supxlabel('Years', fontsize=16)  # Augmenter la taille de l'étiquette de l'axe x
    fig.supylabel('Tariff Revenue (EUR)', fontsize=16)  # Augmenter la taille de l'étiquette de l'axe y

    # Ajouter une légende commune en bas de la figure
    handles, labels = ax.get_legend_handles_labels()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "revenue_tariff_comparison.png"), dpi=350)
    
    return None



def plot_storage_revenues(STORAGE_RESULT, params, categories, output_dir):
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))

    bar_width = 0.25
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for idx, (scenario, df_delta) in enumerate(STORAGE_RESULT.items()):
        # Calculer les revenus
        df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
        df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
        df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']
        
        annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
        annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
        annual_total_revenue = df_delta.groupby('year')['revenue_net'].sum().tolist()
        
        # Calculer les revenus annuels moyens
        average_market_revenue = np.mean(annual_market_revenue)
        average_tariff_revenue = np.mean(annual_tariff_revenue)
        average_total_revenue = np.mean(annual_total_revenue)

        # Lire le delta
        delta = float(params[scenario]['global']['tariff']['delta'])
        
        # Préparer les données pour les bar charts
        revenues = [average_market_revenue, average_tariff_revenue, average_total_revenue]
        
        # Calculer les pourcentages par rapport au revenu total
        market_percentage = (average_market_revenue / average_total_revenue) * 100
        tariff_percentage = (average_tariff_revenue / average_total_revenue) * 100
        
        # Obtenir l'axe pour le subplot actuel
        ax = axes[idx // 3, idx % 3]
        
        # Tracer les bar charts sans hachures mais avec des bordures noires
        bars = []
        for i, (revenue, color) in enumerate(zip(revenues, colors)):
            bar = ax.bar(i, revenue, bar_width, color=color, edgecolor='black')
            bars.append(bar)
        
        # Ajouter le titre avec le delta
        ax.set_title(f'Δ: {delta:.2f}')
        ax.set_xticks(np.arange(len(categories)))
        ax.set_xticklabels(categories, rotation=0, ha='right')
        
        # Annoter chaque barre avec sa valeur ou le pourcentage
        for i, bar in enumerate(bars):
            for rect in bar:
                height = rect.get_height()
                if i == 0:  # market revenue
                    annotation = f'{market_percentage:.2f}%'
                elif i == 1:  # tariff revenue
                    annotation = f'{tariff_percentage:.2f}%'
                else:  # total revenue
                    annotation = ''
                ax.annotate(annotation, 
                            xy=(rect.get_x() + rect.get_width() / 2, height), 
                            xytext=(0, 3), 
                            textcoords='offset points', 
                            ha='center', 
                            fontsize=8)
        
        # Afficher les labels des axes x et y uniquement pour les subplots en bas et à gauche
        if idx // 3 == 2:
            ax.set_xlabel('Revenue Types')
        if idx % 3 == 0:
            ax.set_ylabel('Average Revenue (EUR/y)')
        
        ax.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_delta.png"), dpi=350)
    return None



def plot_stacked_revenues(STORAGE_RESULT, params, output_dir):
    
    deltas = []
    average_market_revenues = []
    average_tariff_revenues = []
    average_total_revenues = []

    for scenario, df_delta in STORAGE_RESULT.items():
        # Calculer les revenus
        df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
        df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
        df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']
        
        # Calculer les revenus moyens
        annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
        annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
        annual_total_revenue = df_delta.groupby('year')['revenue_net'].sum().tolist()
        
        # Calculer les revenus annuels moyens
        average_market_revenue = np.mean(annual_market_revenue)
        average_tariff_revenue = np.mean(annual_tariff_revenue)
        average_total_revenue = np.mean(annual_total_revenue)

        # Lire le delta
        delta = float(params[scenario]['global']['tariff']['delta'])
        
        # Stocker les valeurs
        deltas.append(delta)
        average_market_revenues.append(average_market_revenue)
        average_tariff_revenues.append(average_tariff_revenue)
        average_total_revenues.append(average_total_revenue)

    # Tracer le bar chart empilé
    fig, ax = plt.subplots(figsize=(12, 8))

    bar_width = 0.35
    index = np.arange(len(deltas))
    
    bars1 = ax.bar(index, average_market_revenues, bar_width, label='Market Revenue', color='#1f77b4', hatch='/')
    bars2 = ax.bar(index, average_tariff_revenues, bar_width, bottom=average_market_revenues, label='Tariff Revenue', color='#ff7f0e', hatch='\\')
    bars3 = ax.bar(index, average_total_revenues, bar_width, bottom=np.array(average_market_revenues) + np.array(average_tariff_revenues), label='Total Revenue', color='#2ca02c', hatch='x')

    ax.set_xlabel('Δ')
    ax.set_ylabel('Average Revenue (EUR/y)')
    #ax.set_title('Average Revenue by Delta')
    ax.set_xticks(index)
    ax.set_xticklabels([f'{delta:.2f}' for delta in deltas])
    ax.legend()

    # Annoter chaque barre avec sa valeur
    def annotate_bars(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2), 
                        xytext=(0, 3), 
                        textcoords='offset points', 
                        ha='center', 
                        fontsize=8)

    annotate_bars(bars1)
    annotate_bars(bars2)
    annotate_bars(bars3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_delta_stacked.png"), dpi=350)
    
    return None 


def plot_stacked_revenues_2(STORAGE_RESULT, params, output_dir):
    
    deltas = []
    average_market_revenues = []
    average_tariff_revenues = []

    for scenario, df_delta in STORAGE_RESULT.items():
        # Calculer les revenus
        df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
        df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
        df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']
        
        # Calculer les revenus annuels moyens
        annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
        annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
        
        # Calculer les revenus moyens
        average_market_revenue = np.mean(annual_market_revenue)
        average_tariff_revenue = np.mean(annual_tariff_revenue)

        # Lire le delta
        delta = float(params[scenario]['global']['tariff']['delta'])
        
        # Stocker les valeurs
        deltas.append(delta)
        average_market_revenues.append(average_market_revenue)
        average_tariff_revenues.append(average_tariff_revenue)

    # Tracer le bar chart empilé
    fig, ax = plt.subplots(figsize=(12, 8))

    bar_width = 0.35
    index = np.arange(len(deltas))
    
    bars1 = ax.bar(index, average_market_revenues, bar_width, label='Market Revenue', color='#1f77b4')
    bars2 = ax.bar(index, average_tariff_revenues, bar_width, bottom=average_market_revenues, label='Tariff Revenue', color='#ff7f0e')

    ax.set_xlabel('Δ')
    ax.set_ylabel('Average Revenue (EUR/y)')
    ax.set_xticks(index)
    ax.set_xticklabels([f'{delta:.2f}' for delta in deltas])
    ax.legend()

    # Annoter chaque barre avec sa valeur au milieu des barres
    def annotate_bars(bars, revenues):
        for bar, revenue in zip(bars, revenues):
            height = bar.get_height()
            ax.annotate(f'{height:.2f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2), 
                        xytext=(0, 0), 
                        textcoords='offset points', 
                        ha='center', 
                        va='center', 
                        color='white',
                        fontsize=8,
                        rotation=90)

    annotate_bars(bars1, average_market_revenues)
    annotate_bars(bars2, average_tariff_revenues)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_delta_stacked_2.png"), dpi=350)
    return None



def plot_stacked_revenues_3(STORAGE_RESULT, params, output_dir):
    
    deltas = []
    average_market_revenues = []
    average_tariff_revenues = []

    for scenario, df_delta in STORAGE_RESULT.items():
        # Calculer les revenus
        df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
        df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
        df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']
        
        # Calculer les revenus annuels moyens
        annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
        annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
        
        # Calculer les revenus moyens
        average_market_revenue = np.mean(annual_market_revenue)
        average_tariff_revenue = np.mean(annual_tariff_revenue)

        # Lire le delta
        delta = float(params[scenario]['global']['tariff']['delta'])
        
        # Stocker les valeurs
        deltas.append(delta)
        average_market_revenues.append(average_market_revenue)
        average_tariff_revenues.append(average_tariff_revenue)

    # Tracer le bar chart empilé
    fig, ax = plt.subplots(figsize=(8, 6))

    bar_width = 0.35
    index = np.arange(len(deltas))
    
    bars1 = ax.bar(index, average_market_revenues, bar_width, label='Market Revenue', color='#1f77b4', edgecolor='black')
    bars2 = ax.bar(index, average_tariff_revenues, bar_width, bottom=average_market_revenues, label='Tariff Revenue', color='#ff7f0e', edgecolor='black')

    ax.set_xlabel('Δ', fontsize=16)
    ax.set_ylabel('Average Revenue (EUR/y)', fontsize=14)
    ax.set_xticks(index)
    ax.set_xticklabels([f'{delta:.2f}' for delta in deltas], fontsize=14)
    ax.legend(fontsize=12)

    # Annoter chaque barre avec le pourcentage de sa valeur par rapport à la somme des valeurs des barres empilées
    def annotate_bars(bars, revenues, total_revenues):
        for bar, revenue, total_revenue in zip(bars, revenues, total_revenues):
            percentage = (revenue / total_revenue) * 100
            ax.annotate(f'{percentage:.2f}%', 
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2), 
                        xytext=(0, 0), 
                        textcoords='offset points', 
                        ha='center', 
                        va='center', 
                        color='white',
                        fontsize=10,
                        rotation=90)

    total_revenues = np.array(average_market_revenues) + np.array(average_tariff_revenues)
    annotate_bars(bars1, average_market_revenues, total_revenues)
    annotate_bars(bars2, average_tariff_revenues, total_revenues)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_delta_stacked_3.png"), dpi=350)
    return None


def plot_stacked_revenues_by_shape(STORAGE_RESULT, params, output_dir):
    # Obtenir toutes les formes uniques
    shapes = sorted(set(params[scenario]['global']['tariff']['shape'] for scenario in STORAGE_RESULT.keys()))
    colors = ['#1f77b4', '#ff7f0e']  # Couleurs pour Market Revenue et Tariff Revenue
    hatches = ['/', '\\']
    bar_width=0.4

    fig, axes = plt.subplots(len(shapes), 1, figsize=(12, 8 * len(shapes)))

    if len(shapes) == 1:
        axes = [axes]  # S'assurer que axes soit toujours une liste

    for shape_idx, shape in enumerate(shapes):
        shares = []
        average_market_revenues = []
        average_tariff_revenues = []

        for scenario, df_delta in STORAGE_RESULT.items():
            if params[scenario]['global']['tariff']['shape'] == shape:
                # Calculer les revenus
                df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
                df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
                df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']

                # Calculer les revenus annuels moyens
                annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
                annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
                
                # Calculer les revenus moyens
                average_market_revenue = np.mean(annual_market_revenue)
                average_tariff_revenue = np.mean(annual_tariff_revenue)

                # Lire le share
                share = float(params[scenario]['global']['tariff']['share'])
                
                # Stocker les valeurs
                shares.append(share)
                average_market_revenues.append(average_market_revenue)
                average_tariff_revenues.append(average_tariff_revenue)

        # Convertir les listes en arrays numpy
        shares = np.array(shares)
        average_market_revenues = np.array(average_market_revenues)
        average_tariff_revenues = np.array(average_tariff_revenues)

        # Tracer les bar charts pour la forme actuelle
        ax = axes[shape_idx]
        index = np.arange(len(shares))
        
        bars1 = ax.bar(index, average_market_revenues, bar_width, label='Market Revenue', color=colors[0], hatch=hatches[0])
        bars2 = ax.bar(index, average_tariff_revenues, bar_width, bottom=average_market_revenues, label='Tariff Revenue', color=colors[1], hatch=hatches[1])

        # Ajouter les annotations
        for bar1, bar2 in zip(bars1, bars2):
            height1 = bar1.get_height()
            height2 = bar2.get_height()
            total_height = height1 + height2
            ax.annotate(f'{total_height:.2f}', 
                        xy=(bar1.get_x() + bar1.get_width() / 2, total_height), 
                        xytext=(0, 3), 
                        textcoords='offset points', 
                        ha='center', 
                        fontsize=8)

        ax.set_xlabel('share')
        ax.set_ylabel('Average Revenue (EUR/y)')
        ax.set_title(f'{shape} tariff')
        ax.set_xticks(index)
        ax.set_xticklabels([f'{share:.2f}' for share in shares])
        ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_share_and_shape_stacked.png"), dpi=350)
    
    return None


def plot_stacked_revenues_by_shape_horizontal(STORAGE_RESULT, params, output_dir):
    # Obtenir toutes les formes uniques
    shapes = sorted(set(params[scenario]['global']['tariff']['shape'] for scenario in STORAGE_RESULT.keys()))
    colors = ['#1f77b4', '#ff7f0e']  # Couleurs pour Market Revenue et Tariff Revenue
    hatches = ['/', '\\']
    bar_width = 0.3

    # Modifier les subplots pour qu'ils soient horizontaux
    fig, axes = plt.subplots(1, len(shapes), figsize=(7 * len(shapes), 5))

    if len(shapes) == 1:
        axes = [axes]  # S'assurer que axes soit toujours une liste

    for shape_idx, shape in enumerate(shapes):
        shares = []
        average_market_revenues = []
        average_tariff_revenues = []

        for scenario, df_delta in STORAGE_RESULT.items():
            if params[scenario]['global']['tariff']['shape'] == shape:
                # Calculer les revenus
                df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
                df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
                df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']

                # Calculer les revenus annuels moyens
                annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
                annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
                
                # Calculer les revenus moyens
                average_market_revenue = np.mean(annual_market_revenue)
                average_tariff_revenue = np.mean(annual_tariff_revenue)

                # Lire le share
                share = float(params[scenario]['global']['tariff']['share'])
                
                # Stocker les valeurs
                shares.append(share)
                average_market_revenues.append(average_market_revenue)
                average_tariff_revenues.append(average_tariff_revenue)

        # Convertir les listes en arrays numpy
        shares = np.array(shares)
        average_market_revenues = np.array(average_market_revenues)
        average_tariff_revenues = np.array(average_tariff_revenues)

        # Tracer les bar charts pour la forme actuelle
        ax = axes[shape_idx]
        index = np.arange(len(shares))
        
        bars1 = ax.bar(index, average_market_revenues, bar_width, label='Market Revenue', color=colors[0], hatch=hatches[0])
        bars2 = ax.bar(index, average_tariff_revenues, bar_width, bottom=average_market_revenues, label='Tariff Revenue', color=colors[1], hatch=hatches[1])

        # Ajouter les annotations
        for bar1, bar2 in zip(bars1, bars2):
            height1 = bar1.get_height()
            height2 = bar2.get_height()
            total_height = height1 + height2

            # Ajouter l'annotation pour le total
            ax.annotate(f'{total_height:.2f}', 
                        xy=(bar1.get_x() + bar1.get_width() / 2, total_height), 
                        xytext=(0, 3), 
                        textcoords='offset points', 
                        ha='center', 
                        fontsize=10)

            # Ajouter les annotations pour les pourcentages
            market_pct = (height1 / total_height) * 100 if total_height > 0 else 0
            tariff_pct = (height2 / total_height) * 100 if total_height > 0 else 0

            ax.annotate(f'{market_pct:.1f}%', 
                        xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2), 
                        xytext=(0, 0), 
                        textcoords='offset points', 
                        ha='center', 
                        color='white',
                        fontsize=10)
            
            ax.annotate(f'{tariff_pct:.1f}%', 
                        xy=(bar2.get_x() + bar2.get_width() / 2, height1 + height2 / 2), 
                        xytext=(0, 0), 
                        textcoords='offset points', 
                        ha='center', 
                        color='white',
                        fontsize=10)

        ax.set_xlabel('share')
        ax.set_ylabel('Average Revenue (EUR/y)')
        ax.set_title(f'{shape} Tariff')
        ax.set_xticks(index)
        ax.set_xticklabels([f'{share:.2f}' for share in shares])
        ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_share_and_shape_stacked_horizontal.png"), dpi=400)
    
    return None

def plot_stacked_revenues_by_shape_vertical(STORAGE_RESULT, params, output_dir):
    # Obtenir toutes les formes uniques
    shapes = sorted(set(params[scenario]['global']['tariff']['shape'] for scenario in STORAGE_RESULT.keys()))
    colors = ['#1f77b4', '#ff7f0e']  # Couleurs pour Market Revenue et Tariff Revenue
    bar_width = 0.4

    fig, axes = plt.subplots(len(shapes), 1, figsize=(6, 4 * len(shapes)))

    if len(shapes) == 1:
        axes = [axes]  # S'assurer que axes soit toujours une liste

    for shape_idx, shape in enumerate(shapes):
        shares = []
        average_market_revenues = []
        average_tariff_revenues = []

        for scenario, df_delta in STORAGE_RESULT.items():
            if params[scenario]['global']['tariff']['shape'] == shape:
                # Calculer les revenus
                df_delta['revenue_net'] = df_delta['dispatch'] * df_delta['price']
                df_delta['revenue_tariff'] = df_delta['dispatch'] * df_delta['tariff']
                df_delta['revenue_market'] = df_delta['dispatch'] * df_delta['base_price']

                # Calculer les revenus annuels moyens
                annual_market_revenue = df_delta.groupby('year')['revenue_market'].sum().tolist()
                annual_tariff_revenue = df_delta.groupby('year')['revenue_tariff'].sum().tolist()
                
                # Calculer les revenus moyens
                average_market_revenue = np.mean(annual_market_revenue)
                average_tariff_revenue = np.mean(annual_tariff_revenue)

                # Lire le share
                share = float(params[scenario]['global']['tariff']['share'])
                
                # Stocker les valeurs
                shares.append(share)
                average_market_revenues.append(average_market_revenue)
                average_tariff_revenues.append(average_tariff_revenue)

        # Convertir les listes en arrays numpy
        shares = np.array(shares)
        average_market_revenues = np.array(average_market_revenues)
        average_tariff_revenues = np.array(average_tariff_revenues)

        # Tracer les bar charts pour la forme actuelle
        ax = axes[shape_idx]
        index = np.arange(len(shares))
        
        bars1 = ax.bar(index, average_market_revenues, bar_width, label='Market Revenue', color=colors[0], edgecolor='black')
        bars2 = ax.bar(index, average_tariff_revenues, bar_width, bottom=average_market_revenues, label='Tariff Revenue', color=colors[1], edgecolor='black')

        # Ajouter les annotations pour les pourcentages
        for bar1, bar2 in zip(bars1, bars2):
            height1 = bar1.get_height()
            height2 = bar2.get_height()
            total_height = height1 + height2

            if total_height > 0:
                market_pct = (height1 / total_height) * 100
                tariff_pct = (height2 / total_height) * 100

                # Ajuster les pourcentages pour qu'ils ne dépassent pas 100%
                market_pct = min(market_pct, 100)
                tariff_pct = min(tariff_pct, 100 - market_pct)

                ax.annotate(f'{market_pct:.1f}%', 
                            xy=(bar1.get_x() + bar1.get_width() / 2, height1 / 2), 
                            xytext=(0, 0), 
                            textcoords='offset points', 
                            ha='center', 
                            color='white',
                            fontsize=7)
                
                ax.annotate(f'{tariff_pct:.1f}%', 
                            xy=(bar2.get_x() + bar2.get_width() / 2, height1 + height2 / 2), 
                            xytext=(0, 0), 
                            textcoords='offset points', 
                            ha='center', 
                            color='black',
                            rotation='vertical',
                            fontsize=7)

        ax.set_xlabel('share')
        ax.set_ylabel('Average Revenue (EUR/y)')
        ax.set_title(f'{shape}')
        ax.set_xticks(index)
        ax.set_xticklabels([f'{share:.2f}' for share in shares])
        ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Sensitivity_on_share_and_shape_stacked_vertical.png"), dpi=350)
    return None






