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

% Boucle sur chaque scénario pour tracer la relation revenue vs net_load
for i = 1:length(scenarios)
    subplot(2, 2, i); % Création d'un subplot (2x2)
    hold on;
    
    % Extraction des colonnes Pd, price et net_load
    Pd = data{i}.Pd;  % Puissance demandée
    price = data{i}.price; % Prix
    net_load = data{i}.net_load; % Charge nette
    revenue = Pd .* price; % Calcul du revenu
    
    % Tracé du scatter plot revenue vs net_load
    scatter(net_load, revenue, 8, colors(i, :), 'filled', 'MarkerFaceAlpha', 0.5);
    
    % Ajustement de l'échelle pour une meilleure visualisation
    xlim([min(net_load) max(net_load)]);
    ylim([min(revenue) max(revenue)]);
    
    % Ajout d'une courbe de tendance polynomiale (ordre 2)
    p = polyfit(net_load, revenue, 2);
    x_fit = linspace(min(net_load), max(net_load), 100);
    y_fit = polyval(p, x_fit);
    plot(x_fit, y_fit, 'k-', 'LineWidth', 2);
    
    % Ajout d'étiquettes et d'un titre
    title(['Revenu vs Net Load - ' scenarios{i}]);
    xlabel('Charge Nette (net\_load)');
    ylabel('Revenu (Pd * Price)');
    grid on;
    legend('Données', 'Tendance (polyfit)', 'Location', 'best');
    
    hold off;
end

% Ajouter un titre général à la figure
sgtitle('Relation entre Revenu (Pd * Price) et Charge Nette (Net Load)');

% Ajustement de l'affichage
set(gcf, 'Position', [100, 100, 1000, 600]); % Ajuster la taille de la figure
