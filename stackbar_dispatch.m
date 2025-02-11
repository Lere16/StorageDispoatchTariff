clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

scenarios = {'Ex-Ante', 'Flat', 'Proportional', 'Piecewise'};

% Chargement des données
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Nombre d'années disponibles dans les données
years = unique(data{1}.year);

% Initialisation de la figure pour le subplot
figure;

% Préparer les données pour les barres empilées
dispatch_data = zeros(length(years), length(scenarios));

for i = 1:length(scenarios)
    for j = 1:length(years)
        subset = data{i}(data{i}.year == years(j), :);
        dispatch_data(j, i) = mean(subset.dispatch); % Moyenne du dispatch par année et scénario
    end
end

% Créer un graphique en barres empilées
bar(years, dispatch_data, 'stacked');

% Ajouter des titres et des labels
xlabel('Année');
ylabel('Dispatch total (kWh)');
title('Impact des Tarifs sur le Dispatch du Stockage');
legend(scenarios, 'Location', 'best');
grid on;
