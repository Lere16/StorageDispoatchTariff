% Load data
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'data', 'input');
LOAD_FILE = fullfile(DATA_PATH, 'actual_consumption_TransnetBW.csv');

opts = detectImportOptions(LOAD_FILE);
opts.VariableNamesLine = 1; % Adjust according to the file
data = readtable(LOAD_FILE, opts);

% Extract the residual load column
residual_load = data.('ResidualLoad_MWh_');

% Plot histogram and probability density function (KDE)
figure;
hold on;

% Normalized histogram
histogram(residual_load, 'Normalization', 'pdf', 'FaceColor', [0.7 0.7 1], 'EdgeColor', 'b');

% Kernel Density Estimation (KDE)
[f, xi] = ksdensity(residual_load);
plot(xi, f, 'r-', 'LineWidth', 2); % KDE curve

% Indicate min and max values
min_val = min(residual_load);
max_val = max(residual_load);
plot([min_val min_val], [0 max(f)], 'k--', 'LineWidth', 1.5);
plot([max_val max_val], [0 max(f)], 'k--', 'LineWidth', 1.5);

% Add labels and title
xlabel('Residual Load (MW)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Probability Density', 'FontSize', 12, 'FontWeight', 'bold');
title('Area TransnetBW', 'FontSize', 14, 'FontWeight', 'bold');
grid on;
legend('Histogram', 'KDE Estimation', 'Min-Max');

% Display min and max values
text(min_val, max(f) * 0.1, sprintf('Min: %.2f MW', min_val), 'Color', 'black', 'FontSize', 10);
text(max_val, max(f) * 0.1, sprintf('Max: %.2f MW', max_val), 'Color', 'black', 'FontSize', 10);

hold off;
