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

% Création de la figure avec des subplots
figure;
n_years = length(years);
n_cols = 3; % Nombre de colonnes de subplots
n_rows = ceil(n_years / n_cols); % Nombre de lignes de subplots pour une disposition optimale

% Pour chaque année, créer un subplot avec les histogrammes
for i = 1:n_years
    subplot(n_rows, n_cols, i);
    hold on;
    for j = 1:length(data)
        % Sélectionner les données de l'année actuelle
        subset = data{j}(data{j}.year == years(i), :);
        % Calcul de l'amplitude du dispatch pour l'année et le scénario
        dispatch_diff = subset.Pd - subset.Pc;
        % Tracer l'histogramme pour l'année et le scénario
        histogram(dispatch_diff, 'FaceColor', colors(j, :), 'DisplayName', scenarios{j}, 'BinWidth', 2);
    end
    % Configuration de chaque subplot
    title(['Année: ', num2str(years(i))]);
    xlabel('Amplitude du Dispatch');
    ylabel('Fréquence');
    legend('show');
    grid on;
    hold off;
end

% Ajustement de la mise en page
sgtitle('Distribution de l\''Amplitude du Dispatch pour chaque Scénario et chaque Année');
