clc; clear; close all;

% Data path definition
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% List of CSV files corresponding to each scenario
selected_files = { 'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Scenario names
scenarios = {'Flat', 'Proportional', 'Piecewise'};

% Base tariff in EUR/MWh
base_tariff = 10.56; 

% Initialize results
years_all = [];
load_reduction_mean = [];
cost_savings = [];

% Loop through each scenario
for i = 1:length(selected_files)
    % Load data
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Extract necessary columns
    gridload = data.gridload;  
    net_load = data.net_load; 
    load_reduction = -gridload + net_load; % Load reduction (MW)
    
    % Calculate hourly cost savings (€)
    cost_reduction = load_reduction * base_tariff; 
    
    % Extract unique years
    years = unique(data.year);
    years_all = unique([years_all; years]); % Store all years
    
    % Calculate the annual average load reduction (excluding zeros)
    mean_reduction = arrayfun(@(year) mean(load_reduction(data.year == year)), years);
    
    % Calculate total annual savings
    total_savings = arrayfun(@(year) sum(cost_reduction(data.year == year & load_reduction ~= 0)), years);
    
    % Store results
    load_reduction_mean = [load_reduction_mean; mean_reduction(:)'];
    cost_savings = [cost_savings; total_savings(:)'];
end

% Create figure with 2 subplots
figure;

% Subplot 1: Average Load Reduction
subplot(2,1,1);
bar(years_all, load_reduction_mean', 'grouped');
xlabel('Year');
ylabel('Avg. Load Reduction (MW/h)');
%title('Comparison of Average Load Reduction by Scenario');
title('a)');
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);

% Subplot 2: Annual Savings
subplot(2,1,2);
plot(years_all, cost_savings', '-o', 'LineWidth', 2);
xlabel('Year');
ylabel('Annual Savings (€)');
%title('Annual Savings Due to Load Reduction');
title('b)')
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);

% Adjust figure layout
%sgtitle('Impact of Storage: Load Reduction and Annual Savings');
set(gcf, 'Position', [100, 100, 800, 600]); % Adjust figure size
