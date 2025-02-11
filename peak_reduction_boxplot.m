clc; clear; close all;



% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'without tariff', 'Flat', 'Proportional', 'Piecewise'};


% Initialisation des résultats
all_reductions = [];

% Boucle sur chaque scénario
for i = 1:length(selected_files)
    % Chargement des données
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Calcul de la réduction de charge
    gridload = data.gridload;  
    net_load = data.net_load; 
    load_reduction = gridload - net_load;
    
    % Stocker les résultats
    all_reductions = [all_reductions, load_reduction];
end

% Création du boxplot
figure;
boxplot(all_reductions, scenarios, 'Symbol', 'o');
xlabel('Scénario');
ylabel('Réduction de Charge (MW)');
title('Analyse de la Variabilité de la Réduction de Charge');
grid on;
set(gca, 'FontSize', 12);
