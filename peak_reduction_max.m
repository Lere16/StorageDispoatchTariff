clc; clear; close all;
%OK
% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/Amprion');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_CONFIGURATION_scenario_22.csv', ...
                   'storage_result_CONFIGURATION_scenario_23.csv', ...
                   'storage_result_CONFIGURATION_scenario_24.csv', ...
                   'storage_result_CONFIGURATION_scenario_25'};

% Noms des scénarios
scenarios = {'scenario_22', 'scenario_23', 'scenario_24', 'scenario_25' };

% Initialize results
years_all = [];
peak_reduction = [];
relative_reduction = [];

% Loop through each scenario
for i = 1:length(selected_files)
    % Load data
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Extract unique years
    years = unique(round(data.year));
    years_all = unique([years_all; years]); % Store all years
    
    % Initialize vectors for each scenario
    peak_reduction_scenario = zeros(size(years));
    relative_reduction_scenario = zeros(size(years));
    
    % Loop through each year
    for j = 1:length(years)
        year = years(j);
        idx = (data.year == year);
        
        % Compute peak reduction
        peak_gridload = max(data.gridload(idx)); % Peak load without storage
        peak_netload = max(data.dispatch_load(idx)); % Peak load with storage
        reduction = peak_gridload - peak_netload;
        
        % Compute relative reduction
        rel_reduction = (reduction / peak_gridload) * 100;
        
        % Store results
        peak_reduction_scenario(j) = reduction;
        relative_reduction_scenario(j) = rel_reduction;
    end
    
    % Store results for all scenarios
    peak_reduction = [peak_reduction; peak_reduction_scenario(:)'];
    relative_reduction = [relative_reduction; relative_reduction_scenario(:)'];
end

% Create figure with 2 subplots
figure;

% Subplot 1: Peak Reduction in MW
subplot(2,1,1);
bar(years_all, peak_reduction', 'grouped');
xlabel('Year');
ylabel('Peak Reduction (MW)');
title('Comparison of Peak Load Reduction by Scenario');
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);

% Subplot 2: Relative Peak Reduction (%)
subplot(2,1,2);
plot(years_all, relative_reduction', '-o', 'LineWidth', 2);
xticks(unique(data.year))
xlabel('Year');
ylabel('Relative Peak Reduction (%)');
title('Relative Reduction of Peak Load');
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);

% Adjust figure layout
sgtitle('Impact of Storage: Peak Load Reduction Analysis');
set(gcf, 'Position', [100, 100, 800, 600]); % Adjust figure size
