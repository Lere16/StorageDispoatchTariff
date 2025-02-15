clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/100/germany');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'without tariff', 'Flat', 'Proportional', 'Piecewise'};

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
        peak_netload = max(data.net_load(idx)); % Peak load with storage
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

% Create figure
figure;

% Peak Reduction in MW (improved version)
bar_handle = bar(years_all, peak_reduction', 'grouped');
xlabel('Year');
ylabel('Peak Reduction (MW)');
title('50Hertz');
legend(scenarios, 'Location', 'best');
%grid on;
set(gca, 'FontSize', 12);

% Display the values on the bars
for i = 1:length(bar_handle)
    xtips1 = bar_handle(i).XEndPoints;
    ytips1 = bar_handle(i).YEndPoints;
    labels1 = string(bar_handle(i).YData);
    text(xtips1, ytips1, labels1, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', 'FontSize', 10, 'FontWeight', 'bold');
end

% Customizing bar appearance
colormap autumn; % Changing the color of the bars
set(bar_handle, 'EdgeColor', 'k', 'LineWidth', 1.5); % Adding edge color to bars

% Adjust figure layout
%sgtitle('Impact of Storage: Peak Load Reduction Analysis');
set(gcf, 'Position', [100, 100, 800, 600]); % Adjust figure size
