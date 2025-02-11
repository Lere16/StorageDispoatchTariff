clc; clear; close all;
% MEAN 


% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'Flat', 'Proportional', 'Piecewise'};

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
    
    % Calcul de la moyenne annuelle de la réduction de charge
    mean_reduction = arrayfun(@(year) mean(load_reduction(data.year == year)), years);
    
    % Stockage des résultats
    load_reduction_mean = [load_reduction_mean; mean_reduction(:)'];
end

% Création du graphique en barres
figure;
bar(years_all, load_reduction_mean', 'grouped');
xlabel('Année');
ylabel('Réduction Moyenne de Charge (MW)');
title('Comparaison de la Réduction Moyenne de Charge par Scénario');
legend(scenarios, 'Location', 'best');
grid on;
set(gca, 'FontSize', 12);
