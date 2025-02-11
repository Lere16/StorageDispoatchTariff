clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/germany');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'Ex-Ante', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios)); % Couleurs différentes pour chaque scénario

% Chargement des données
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Création d'une figure
figure;

% Boucle sur chaque scénario pour tracer l'évolution des revenus
for i = 1:length(scenarios)
    subplot(2, 2, i); % Création d'un subplot (2x2)
    hold on;
    
    % Extraction des colonnes Pd et price
    Pd = data{i}.Pd;  % Puissance demandée
    price = data{i}.price; % Prix
    revenue = Pd .* price; % Calcul du revenu
    
    % Tracé du revenu en fonction du temps (index des données)
    plot(1:length(revenue), revenue, 'Color', colors(i, :), 'LineWidth', 1.5);
    
    % Ajout d'une courbe de tendance lissée (moving average)
    windowSize = 24; % Lissage sur 24 heures (ajuster selon besoin)
    smooth_revenue = movmean(revenue, windowSize);
    plot(1:length(revenue), smooth_revenue, '--', 'Color', colors(i, :), 'LineWidth', 2);
    
    % Ajout d'étiquettes et d'un titre
    title(['Revenus Pd * Price - ' scenarios{i}]);
    xlabel('Temps (heures ou index)');
    ylabel('Revenu (monnaie locale)');
    grid on;
    legend('Revenu brut', 'Tendance lissée', 'Location', 'best');
    
    hold off;
end

% Ajouter un titre général à la figure
sgtitle('Évolution des revenus (Pd * Price) pour chaque scénario');

% Ajustement de l'affichage
set(gcf, 'Position', [100, 100, 1000, 600]); % Ajuster la taille de la figure
