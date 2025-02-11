clc; clear; close all;

% Define data path
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% List of CSV files corresponding to each scenario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Scenario names
scenarios = {'Ex-Ante', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios)); % Different colors for each scenario

% Load data
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Create figure
figure;

% Loop through each scenario to plot revenue vs net_load relationship
for i = 1:length(scenarios)
    subplot(2, 2, i); % Create a 2x2 subplot
    hold on;
    
    % Extract columns Pd, price, and net_load
    Pd = data{i}.Pd;  % Power demand
    price = data{i}.price; % Price
    net_load = data{i}.net_load; % Net load
    revenue = Pd .* price; % Compute revenue
    
    % Plot scatter plot revenue vs net_load
    scatter(net_load, revenue, 8, colors(i, :), 'filled', 'MarkerFaceAlpha', 0.5);
    
    % Adjust scale for better visualization
    xlim([min(net_load) max(net_load)]);
    ylim([min(revenue) max(revenue)]);
    
    % Add a polynomial trend curve (order 2)
    p = polyfit(net_load, revenue, 2);
    x_fit = linspace(min(net_load), max(net_load), 100);
    y_fit = polyval(p, x_fit);
    plot(x_fit, y_fit, 'k-', 'LineWidth', 2);
    
    % Add labels and title
    title([scenarios{i}]);
    xlabel('Net Load (MW)');
    ylabel('Revenue (€)');
    grid on;
    legend('Data', 'Trend (polyfit)', 'Location', 'best');
    
    hold off;
end

% Add a general title to the figure
%sgtitle('Relationship Between Revenue (Pd * Price) and Net Load');

% Adjust display settings
set(gcf, 'Position', [100, 100, 1000, 600]); % Adjust figure size
