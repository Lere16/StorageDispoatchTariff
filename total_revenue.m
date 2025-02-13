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

% Initialisation des matrices pour stocker les moyennes et écarts-types
avg_revenue_market = zeros(length(scenarios), 1);
avg_revenue_tariff = zeros(length(scenarios), 1);
std_revenue_market = zeros(length(scenarios), 1);
std_revenue_tariff = zeros(length(scenarios), 1);

% Boucle sur chaque scénario pour calculer les revenus moyens et écarts-types
for i = 1:length(scenarios)
    % Chargement des données
    filename = fullfile(DATA_PATH, selected_files{i});
    data = readtable(filename);
    
    % Vérifier si les colonnes nécessaires existent
    if ~all(ismember({'dispatch', 'base_price', 'tariff', 'year'}, data.Properties.VariableNames))
        error('Une colonne nécessaire est absente du fichier %s', selected_files{i});
    end

    % Extraction des années uniques
    years = unique(data.year);
    num_years = length(years); % Nombre total d'années de simulation
    
    % Initialisation des revenus annuels
    revenue_market = zeros(num_years, 1);
    revenue_tariff = zeros(num_years, 1);
    
    for j = 1:num_years
        idx = data.year == years(j);
        revenue_market(j) = sum(data.dispatch(idx) .* data.base_price(idx)); % Somme annuelle
        revenue_tariff(j) = sum(data.dispatch(idx) .* data.tariff(idx)); % Somme annuelle
    end
    
    % Calcul des revenus moyens annuels
    avg_revenue_market(i) = mean(revenue_market);
    avg_revenue_tariff(i) = mean(revenue_tariff);
    
    % Calcul de l'écart-type
    std_revenue_market(i) = std(revenue_market);
    std_revenue_tariff(i) = std(revenue_tariff);
end

% Création du bar chart avec barres d’erreur
figure;
hold on;

% Création des barres
b = bar([avg_revenue_market, avg_revenue_tariff], 'grouped');

% Position des barres
nbars = size([avg_revenue_market, avg_revenue_tariff], 2);
xPos = nan(nbars, length(scenarios));

for k = 1:nbars
    xPos(k, :) = b(k).XEndPoints; % Positions des barres
end

% Ajout des barres d’erreur
errorbar(xPos(1, :), avg_revenue_market, std_revenue_market, 'k.', 'LineWidth', 1.5);
errorbar(xPos(2, :), avg_revenue_tariff, std_revenue_tariff, 'k.', 'LineWidth', 1.5);

% Ajustement des étiquettes d'axe X
xticks(mean(xPos, 1));  % Positionne les étiquettes au centre des groupes
xticklabels(scenarios);  % Associe les étiquettes aux scénarios

% Ajout des labels et du titre
ylabel('Average Annual Revenue (€)');
%title('Average Annual Revenue per Scenario');
legend('Market-based', 'Tariff-based', 'Location', 'best');
grid on;
hold off;

% Ajustement de la taille de la figure
set(gcf, 'Position', [100, 100, 800, 500]);
