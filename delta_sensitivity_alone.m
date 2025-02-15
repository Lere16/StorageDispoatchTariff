clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_5.csv', ...
                   'storage_result_scenario_6.csv', ...
                   'storage_result_scenario_7.csv', ...
                   'storage_result_scenario_8.csv', ...
                   'storage_result_scenario_9.csv', ...
                   'storage_result_scenario_10.csv', ...
                   'storage_result_scenario_11.csv', ...
                   'storage_result_scenario_12.csv', ...
                   };

% Noms des scénarios
scenarios = {'0.05', '0.07', '0.09', '0.11','0.13', '0.15', '0.17', '0.19'};

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

% Premier subplot: Revenus empilés
bar_data = [average_market_revenues; average_tariff_revenues]';
bar(deltas, bar_data, 'stacked');
set(gca, 'XTick', deltas, 'XTickLabel', scenarios); % Définit les étiquettes des abscisse
xlabel('\Delta');
ylabel('Average Revenue (EUR/y)');
% Placer la légende en bas, de manière horizontale
legend({'Energy market revenue', 'Tariff-based Revenue'}, 'Location', 'southoutside', 'Orientation', 'horizontal');
set(gca, 'FontSize', 12);
%title('a');

% Ajustement de la taille de la figure
set(gcf, 'Position', [100, 100, 800, 400]);
