clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

scenarios = {'scenario_1', 'scenario_2', 'scenario_3', 'scenario_4'};
colors = lines(length(scenarios));

% Chargement des données
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Nombre d'années disponibles dans les données
years = unique(data{1}.year);

% Initialisation de la figure
figure;

% Pour chaque scénario, calculer la fréquence d'activation du stockage
activation_counts = zeros(length(scenarios), length(years));

for i = 1:length(years)
    for j = 1:length(data)
        % Sélectionner les données de l'année actuelle
        subset = data{j}(data{j}.year == years(i), :);
        
        % Identifier les heures où le stockage est activé (Pd > 0 ou Pc < 0)
        activation_hours = sum(subset.Pd > 0 | subset.Pc < 0); 
        
        % Stocker les résultats d'activation par scénario et année
        activation_counts(j, i) = activation_hours;
    end
end

% Création du graphique à barres pour comparer l'activation du stockage
bar(activation_counts', 'grouped'); % Barres groupées par année et scénario
xticks(1:length(years));
xticklabels(years);
xlabel('Année');
ylabel('Nombre d''heures d''activation du stockage');
legend(scenarios, 'Location', 'northeast');
title('Fréquence d\''activation du stockage par Scénario et Année');
grid on;
