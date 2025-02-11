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

% Créer un graphique radar
figure;

% Calculer la moyenne pour chaque scénario et année
mean_dispatch = zeros(length(scenarios), length(years));
for i = 1:length(scenarios)
    for j = 1:length(years)
        subset = data{i}(data{i}.year == years(j), :);
        mean_dispatch(i, j) = mean(-subset.Pc - subset.Pd);
    end
end

% Tracer le graphique radar
theta = linspace(0, 2*pi, length(years)+1); % Ajouter une valeur pour fermer le cercle
hold on;
for i = 1:length(scenarios)
    plot(theta, [mean_dispatch(i,:), mean_dispatch(i,1)], 'LineWidth', 2, 'DisplayName', scenarios{i});
end

% Personnaliser l'affichage
set(gca, 'xtick', theta(1:end-1), 'xticklabel', years);
title('Comparaison du Dispatch pour chaque Scénario');
legend('Location', 'best');
