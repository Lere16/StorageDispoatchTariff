clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_13.csv', ...
                   'storage_result_scenario_14.csv', ...
                   'storage_result_scenario_15.csv', ...
                   'storage_result_scenario_16.csv', ...
                   'storage_result_scenario_17.csv', ...
                   'storage_result_scenario_18.csv'};

% Noms des scénarios
scenarios = {'0.4', '0.5', '0.6', '0.7','0.8', '0.9'};

% Initialisation des variables
deltas = [];
average_market_revenues = [];
average_tariff_revenues = [];

for i = 1:length(selected_files)
    % Charger les données
    file_path = fullfile(DATA_PATH, selected_files{i});
    data = readtable(file_path);
    
    % Calcul des revenus
    data.revenue_market = data.dispatch .* data.base_price;
    data.revenue_tariff = data.dispatch .* data.tariff;
    
    % Calcul des revenus annuels moyens
    annual_market_revenue = varfun(@sum, data, 'InputVariables', 'revenue_market', 'GroupingVariables', 'year');
    annual_tariff_revenue = varfun(@sum, data, 'InputVariables', 'revenue_tariff', 'GroupingVariables', 'year');
    
    % Moyenne sur les années
    avg_market_rev = mean(annual_market_revenue.sum_revenue_market);
    avg_tariff_rev = mean(annual_tariff_revenue.sum_revenue_tariff);
    
    % Lire le delta
    delta = i; % À remplacer par la valeur correcte si disponible
    
    % Stockage des valeurs
    deltas = [deltas, delta];
    average_market_revenues = [average_market_revenues, avg_market_rev];
    average_tariff_revenues = [average_tariff_revenues, avg_tariff_rev];
end

% Création de la figure pour le premier graphique uniquement
figure;

% Premier graphique: Revenus empilés
bar_data = [average_market_revenues; average_tariff_revenues]';
bar(deltas, bar_data, 'stacked');
set(gca, 'XTick', deltas, 'XTickLabel', scenarios); % Définit les étiquettes des abscisse
xlabel('share');
ylabel('Average Revenue (€/y)');
legend({'Energy market revenue', 'Tariff-based Revenue'}, 'Location', 'southoutside', 'Orientation', 'horizontal');
%grid on;
set(gca, 'FontSize', 12);
%title('a');

% Ajustement de la taille de la figure
set(gcf, 'Position', [100, 100, 800, 400]); % Taille plus petite
