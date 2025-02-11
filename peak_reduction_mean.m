clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/Amprion');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_CONFIGURATION_scenario_22.csv', ...
                   'storage_result_CONFIGURATION_scenario_23.csv', ...
                   'storage_result_CONFIGURATION_scenario_24.csv', ...
                   'storage_result_CONFIGURATION_scenario_25'};

% Noms des scénarios
scenarios = {'scenario_22', 'scenario_23', 'scenario_24', 'scenario_25' };

% Initialisation des résultats
years_all = [];
load_reduction_mean = [];

% Boucle sur chaque scénario
for i = 1:length(selected_files)
    % Chargement des données
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Extraction des colonnes nécessaires
    gridload = data.gridload;  
    net_load = data.net_load; 
    load_reduction = -gridload + net_load; % Réduction de la charge

    % Extraction des années uniques
    years = unique(data.year);
    years_all = unique([years_all; years]); % Stocker toutes les années
    
    % Calcul de la moyenne annuelle de la réduction de charge (en excluant les valeurs nulles)
    mean_reduction = arrayfun(@(year) mean(load_reduction(data.year == year & load_reduction ~= 0)), years);
    
    % Stockage des résultats
    load_reduction_mean = [load_reduction_mean; mean_reduction(:)'];
end

% Création du graphique en barres
figure;
bar(years_all, load_reduction_mean', 'grouped');
xlabel('Année');
ylabel('Réduction Moyenne de Charge (MW)');
title('Comparaison de la Réduction Moyenne de Charge par Scénario (sans les valeurs nulles)');
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);
