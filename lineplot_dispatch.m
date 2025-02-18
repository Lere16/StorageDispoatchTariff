clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/100/germany');

selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

scenarios = {'Without Tariff', 'Flat', 'Proportional', 'Piecewise'};

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

% Création du graphique en lignes
hold on;
colors = lines(length(scenarios)); % Définit une couleur pour chaque scénario

for i = 1:length(scenarios)
    % Extraire les données de dispatch pour chaque scénario
    dispatch_data = [];
    for j = 1:length(years)
        subset = data{i}(data{i}.year == years(j), :);
        dispatch_data = [dispatch_data, mean(subset.Pd)]; % Moyenne du dispatch pour chaque année
    end

    % Tracer les lignes
    plot(years, dispatch_data, '-o', 'DisplayName', scenarios{i}, 'LineWidth', 2, 'Color', colors(i, :));
end

% Ajouter des titres et des labels
xlabel('Year');
ylabel('Average dispatch (MW/h)');
legend('Location', 'best');
grid on;
