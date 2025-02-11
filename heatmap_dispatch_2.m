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

% Nombre d'heures dans une journée (supposons qu'il y a 24 heures)
hours_in_day = 24;

% Initialisation de la figure pour le heatmap
figure;

% Créer la matrice pour le heatmap
heatmap_data = NaN(length(scenarios), length(years), hours_in_day); % Dimensions: [scénarios, années, heures]

for i = 1:length(scenarios)
    for j = 1:length(years)
        for k = 1:hours_in_day
            % Sélectionner les données de l'année actuelle et de l'heure actuelle pour chaque scénario
            subset = data{i}(data{i}.year == years(j) & data{i}.hour == k, :);
            
            if ~isempty(subset)
                % Calculer la moyenne du dispatch pour cette heure et cette année
                heatmap_data(i, j, k) = mean(-subset.Pc - subset.Pd); % Dispatch moyen
            end
        end
    end
end

% Créer un heatmap avec un dégradé de couleurs uniforme
h = heatmap(years, scenarios, squeeze(mean(heatmap_data, 3)), 'ColorMap', parula, ...
    'Title', 'Impact des Tarifs sur le Dispatch du Stockage (sur l\''année et les heures)', 'CellLabelColor', 'none');

xlabel('Année');
ylabel('Scénarios');
colorbar; % Ajouter une échelle de couleur
