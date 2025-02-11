clc; clear; close all;

% Definition of data path
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% List of CSV files corresponding to each scenario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Scenario names
scenarios = {'Without Tariff', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios)); % Different colors for each scenario

% Loading data
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Creating a figure
figure;

% Loop through each scenario to plot revenue evolution
for i = 1:length(scenarios)
    subplot(2, 2, i); % Creating a subplot (2x2)
    hold on;
    
    % Extracting columns Pd and price
    Pd = data{i}.Pd;  % Requested power
    price = data{i}.price; % Price
    revenue = Pd .* price; % Calculating revenue
    
    % Plotting revenue over time (data index)
    plot(1:length(revenue), revenue, 'Color', colors(i, :), 'LineWidth', 1.5);
    
    % Adding a smoothed trend line (moving average)
    windowSize = 24; % Smoothing over 24 hours (adjust as needed)
    smooth_revenue = movmean(revenue, windowSize);
    plot(1:length(revenue), smooth_revenue, '--', 'Color', colors(i, :), 'LineWidth', 2);
    
    % Adding labels and a title
    title([scenarios{i}]);
    xlabel('Time (h)');
    ylabel('Revenue (€)');
    grid on;
    legend('Gross revenue', 'Smoothed trend', 'Location', 'best');
    
    hold off;
end

% Add a general title to the figure
%sgtitle('Revenue Evolution (Pd * Price) for Each Scenario');

% Adjusting display
set(gcf, 'Position', [100, 100, 1000, 600]); % Adjust figure size
