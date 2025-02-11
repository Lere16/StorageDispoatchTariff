clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'Flat', 'Proportional', 'Piecewise'};

% Tarif de base en EUR/MWh
base_tariff = 10.56; 

% Initialisation des résultats
years_all = [];
cost_savings = [];

% Boucle sur chaque scénario
for i = 1:length(selected_files)
    % Chargement des données
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Extraction des colonnes nécessaires
    gridload = data.gridload;  
    net_load = data.net_load; 
    load_reduction = -gridload + net_load; % Réduction de la charge (MW)
    
    % Calcul de l'économie de coût horaire (€) 
    cost_reduction = load_reduction * base_tariff; 
    
    % Extraction des années uniques
    years = unique(data.year);
    years_all = unique([years_all; years]); % Stocker toutes les années
    
    % Calcul de l'économie annuelle totale
    total_savings = arrayfun(@(year) sum(cost_reduction(data.year == year & load_reduction ~= 0)), years);
    
    % Stockage des résultats
    cost_savings = [cost_savings; total_savings(:)'];
end

% Création du graphique
figure;
plot(years_all, cost_savings', '-o', 'LineWidth', 2);
xlabel('Année');
ylabel('Économie Annuelle (€)');
title('Économie Annuelle Due à la Réduction de Charge');
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);
