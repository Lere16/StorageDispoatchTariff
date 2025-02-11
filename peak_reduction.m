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
colors = lines(length(scenarios)); % Palette de couleurs

% Création de la figure
figure;

% Boucle sur chaque scénario
for i = 1:length(selected_files)
    % Chargement des données
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Extraction des colonnes nécessaires
    gridload = data.gridload;  
    net_load = data.net_load; 
    
    % Calcul de la réduction de la charge (difference entre gridload et net_load)
    load_reduction = gridload + net_load;
    
    % Extraction des années uniques
    years = unique(data.year);
    
    % Calcul de la réduction de la charge moyenne pour chaque année
    avg_reduction = arrayfun(@(year) mean(load_reduction(data.year == year)), years);
    
    % Création du subplot
    subplot(2, 2, i);
    hold on;
    
    % Tracer la réduction moyenne de la charge pour chaque année
    plot(years, avg_reduction, '-o', 'Color', colors(i, :), 'LineWidth', 2);
    
    % Personnalisation des axes et des titres
    xlabel('Année');
    ylabel('Réduction Moyenne de la Charge (MW)');
    title(['Réduction Moyenne de la Charge - ' scenarios{i}]);
    grid on;
    
    % Ajouter une légende pour chaque scénario
    legend(scenarios{i}, 'Location', 'best');
    
    hold off;
end

% Ajouter un titre global
sgtitle('Réduction de la Charge Moyenne par le Stockage pour Chaque Scénario');

% Ajustement de l'affichage
set(gcf, 'Position', [100, 100, 1000, 600]); % Ajuster la taille de la figure
