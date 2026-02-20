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
years_all = [];
peak_reduction = [];

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

    % Extraction des années
    years = unique(round(data.year));
    years_all = unique([years_all; years]); % Stockage des années uniques
    
    % Initialisation des vecteurs pour chaque scénario
    peak_reduction_scenario = zeros(size(years));

    % Boucle sur les années
    for j = 1:length(years)
        year = years(j);
        idx = (data.year == year);
        
        % Calcul de la réduction du pic de charge
        peak_gridload = max(data.gridload(idx)); % Charge maximale sans stockage
        peak_netload = max(data.net_load(idx)); % Charge maximale avec stockage
        reduction = peak_gridload - peak_netload;
        
        % Stockage des résultats
        peak_reduction_scenario(j) = reduction;
    end
    
    % Stockage des résultats de réduction du pic
    peak_reduction = [peak_reduction; peak_reduction_scenario(:)'];
end

% Création d'une figure avec subplots
figure;

% Premier subplot: Revenus empilés
subplot(2,1,1);
bar_data = [average_market_revenues; average_tariff_revenues]';
bar(deltas, bar_data, 'stacked');
set(gca, 'XTick', deltas, 'XTickLabel', scenarios); % Définit les étiquettes des abscisse
xlabel('share');
ylabel('Average Revenue (EUR/y)');
legend({'Energy market revenue', 'Tariff-based Revenue'}, 'Location', 'northwest');
grid on;
set(gca, 'FontSize', 12);
title('a');

% Deuxième subplot: Réduction du pic de charge
subplot(2,1,2);
bar_handle = bar(years_all, peak_reduction', 'grouped');
xlabel('Year');
ylabel('Peak Reduction (MW)');
title('b');
legend(scenarios, 'Location', 'best');
set(gca, 'FontSize', 12);
colormap autumn;
set(bar_handle, 'EdgeColor', 'k', 'LineWidth', 1.1);
set(gcf, 'Position', [100, 100, 800, 800]); % Ajustement de la taille de la figure
