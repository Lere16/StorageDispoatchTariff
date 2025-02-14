clc; clear; close all;

% Définition du chemin des données
DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/100/germany');

% Liste des fichiers CSV correspondant à chaque scénario
selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

% Noms des scénarios
scenarios = {'Without Tariff', 'Flat', 'Proportional', 'Piecewise'};
colors = lines(length(scenarios)); % Couleurs différentes pour chaque scénario

% Création de la figure
figure;

% Boucle sur chaque scénario pour tracer les revenus annuels
for i = 1:length(scenarios)
    % Chargement des données
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Vérifier si la colonne "dispatch" existe
    if ~ismember('dispatch', data.Properties.VariableNames)
        error('La colonne "dispatch" est absente du fichier %s', selected_files{i});
    end

    % Extraction des années uniques
    years = unique(data.year);
    
    % Initialisation des revenus annuels
    revenue_market = zeros(length(years), 1);
    revenue_tariff = zeros(length(years), 1);
    
    for j = 1:length(years)
        idx = data.year == years(j);
        revenue_market(j) = sum(data.dispatch(idx) .* data.base_price(idx)); % Somme annuelle
        revenue_tariff(j) = sum(data.dispatch(idx) .* data.tariff(idx)); % Somme annuelle
    end
    
    % Tracé du bar chart
    subplot(2, 2, i);
    hold on;
    bar(years, [revenue_market, revenue_tariff], 'grouped');
    
    % Ajout des étiquettes et titres
    title([scenarios{i}]);
    xlabel('Year');
    ylabel('Total revenu (€)');
    legend('Market-based', 'Tariff-based', 'Location', 'best');
    %grid on;
    hold off;
end

% Ajustement de l'affichage
%sgtitle('Revenus Annuels du Stockage par Année et Scénario');
set(gcf, 'Position', [100, 100, 1000, 600]);