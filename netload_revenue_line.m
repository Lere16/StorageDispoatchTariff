clc; clear; close all;
%OK
% Define data path
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% List of CSV files corresponding to each scenario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Scenario names
scenarios = {'Ex-Ante', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios)); % Color palette

% Create figure
figure;

% Loop over each scenario
for i = 1:length(selected_files)
    % Load data
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Extract necessary columns
    Pd = data.Pd;  
    price = data.price;  
    net_load = data.net_load; 
    revenue = Pd .* price;  % Compute revenue (Pd * price)
    
    % Sort data for a smooth plot
    [net_load_sorted, idx] = sort(net_load); 
    revenue_sorted = revenue(idx);
    
    % Apply smoothing with movmean (moving average)
    window_size = round(length(revenue_sorted) * 0.02);  % 5% window of the data
    revenue_smoothed = movmean(revenue_sorted, window_size);
    
    % Create subplot
    subplot(2, 2, i);
    hold on;
    
    % Plot smoothed curves
    plot(net_load_sorted, revenue_smoothed, 'Color', colors(i, :), 'LineWidth', 2);
    
    % Customize axes and titles
    xlabel('Net Load (MW)');
    ylabel('Revenue (€)');
    %title(['Revenue vs Net Load - ' scenarios{i}]);
    grid on;
    
    % Add legend
    legend(scenarios{i}, 'Location', 'best');
    
    hold off;
end

% Add global title
%sgtitle('Revenue Evolution (Pd * Price) as a Function of Net Load');

% Adjust display settings
set(gcf, 'Position', [100, 100, 1000, 600]); % Adjust figure size
