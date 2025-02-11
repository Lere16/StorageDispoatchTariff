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

% Initialisation de la figure pour le subplot
figure;

% Création d'un histogramme lissé pour chaque scénario
for i = 1:length(scenarios)
    subplot(2, 2, i); % Création de sous-graphiques
    hold on;

    % Préparation des données pour l'histogramme (pour la colonne dispatch)
    dispatch_data = [];
    for j = 1:length(data)
        dispatch_data = [dispatch_data; data{j}.dispatch]; % Ajouter les valeurs de dispatch pour toutes les années
    end
    
    % Histogramme pour chaque scénario
    histogram(dispatch_data, 'Normalization', 'pdf', 'EdgeColor', colors(i, :), 'FaceColor', colors(i, :), 'FaceAlpha', 0.4); % Normalisation par densité de probabilité
    
    % Estimation de la densité de probabilité (Kernel Density Estimation - KDE)
    [f, xi] = ksdensity(dispatch_data); % KDE
    
    % Courbe KDE
    plot(xi, f, 'LineWidth', 2, 'Color', colors(i, :));
    
    % Ajouter des titres et des labels
    title(['PDF (KDE) - ' scenarios{i}]);
    xlabel('Dispatch (kWh)');
    ylabel('Densité de probabilité');
    grid on;
end

% Ajuster l'affichage global
sgtitle('Distribution de Dispatch pour toutes les années selon chaque scénario de tarification');
