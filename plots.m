% Charger les données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'data', 'input');
LOAD_FILE = fullfile(DATA_PATH, 'actual_consumption_50Hertz.csv');

opts = detectImportOptions(LOAD_FILE);
opts.VariableNamesLine = 1; % Ajuster selon le fichier
data = readtable(LOAD_FILE, opts);

% Extraire la colonne des charges résiduelles
residual_load = data.('ResidualLoad_MWh_');

% Trier les données pour la CDF
sorted_loads = sort(residual_load);
n = length(sorted_loads);
cdf_values = (1:n) / n; % Probabilité cumulative

% Tracer la courbe de distribution cumulative
figure;
plot(sorted_loads, cdf_values, 'b-', 'LineWidth', 2); 
hold on;

% Indiquer les valeurs min et max
min_val = min(sorted_loads);
max_val = max(sorted_loads);
plot([min_val max_val], [0 1], 'r--', 'LineWidth', 1.5); % Lignes indicatrices

% Ajouter labels et titre
xlabel('Net Load (MW)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Cumulative Probability', 'FontSize', 12, 'FontWeight', 'bold');
%title('Distribution des Charges Résiduelles', 'FontSize', 12, 'FontWeight', 'bold');
grid on;
%legend('Distribution cumulative', 'Min-Max');

% Afficher les valeurs min et max
text(min_val, 0.05, sprintf('Min: %.2f MW', min_val), 'Color', 'red', 'FontSize', 10);
text(max_val, 0.95, sprintf('Max: %.2f MW', max_val), 'Color', 'red', 'FontSize', 10);

hold off;
