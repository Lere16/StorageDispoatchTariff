clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

scenarios = {'Ex-Ante', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios));

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

% Création d'un box plot pour chaque scénario
for i = 1:length(scenarios)
    subplot(2, 2, i); % Création de sous-graphiques
    hold on;

    % Préparation des données pour le box plot
    dispatch_data = [];
    year_labels = [];
    for j = 1:length(years)
        % Sélectionner les données de l'année actuelle pour chaque scénario
        subset = data{i}(data{i}.year == years(j), :);
        dispatch_data = [dispatch_data; subset.dispatch]; % Ajouter les dispatch dans une seule matrice
        year_labels = [year_labels; repmat(years(j), length(subset.dispatch), 1)]; % Répéter l'année pour chaque valeur
    end
    
    % Box plot pour chaque scénario avec les données de dispatch pour chaque année
    boxplot(dispatch_data, year_labels, 'Whisker', 1.5);
    
    % Ajouter des titres et des labels
    title(['Distribution du Dispatch - ' scenarios{i}]);
    xlabel('Année');
    ylabel('Dispatch (kWh)');
    grid on;
end

% Ajuster l'affichage global
sgtitle('Distribution du Dispatch pour chaque scénario de tarification');
