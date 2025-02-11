clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% Liste des fichiers CSV
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'Ex-Ante', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios));

% Création de la figure
figure;

for i = 1:length(selected_files)
    data = readtable(fullfile(DATA_PATH, selected_files{i}));

    % Calcul de la réduction de charge
    load_reduction = data.gridload - data.net_load;
    
    subplot(2, 2, i);
    histogram(load_reduction, 'Normalization', 'pdf', 'FaceColor', colors(i, :));
    
    xlabel('Réduction de Charge (MW)');
    ylabel('Densité');
    title(['Distribution de la Réduction - ' scenarios{i}]);
    grid on;
end
sgtitle('Distribution de la Réduction de Charge par le Stockage');
