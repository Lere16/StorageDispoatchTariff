clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV');

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

    % Préparation des données pour le box plot (pour la colonne Pd)
    Pd_data = [];
    year_labels = [];
    for j = 1:length(years)
        % Sélectionner les données de l'année actuelle pour chaque scénario
        subset = data{i}(data{i}.year == years(j), :);
        Pd_data = [Pd_data; subset.Pc]; % Ajouter les valeurs de Pd dans une seule matrice
        year_labels = [year_labels; repmat(years(j), length(subset.Pd), 1)]; % Répéter l'année pour chaque valeur de Pd
    end
    
    % Box plot pour chaque scénario avec les données de Pd pour chaque année
    boxplot(Pd_data, year_labels, 'Whisker', 1.5);
    
    % Ajouter des titres et des labels
    title(['Distribution de Pd - ' scenarios{i}]);
    xlabel('Année');
    ylabel('Pd (kWh)');
    grid on;
end

% Ajuster l'affichage global
sgtitle('Distribution de Pd pour chaque scénario de tarification');
