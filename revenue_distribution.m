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

% Initialisation des matrices pour stocker les moyennes et statistiques
avg_revenue_market = zeros(length(scenarios), 1);
avg_revenue_tariff = zeros(length(scenarios), 1);
std_revenue_market = zeros(length(scenarios), 1);
std_revenue_tariff = zeros(length(scenarios), 1);

% Ajout des valeurs min et max
min_revenue_market = zeros(length(scenarios), 1);
max_revenue_market = zeros(length(scenarios), 1);
min_revenue_tariff = zeros(length(scenarios), 1);
max_revenue_tariff = zeros(length(scenarios), 1);

% Ajout des percentiles pour définir les barres d'erreur
lower_bound_market = zeros(length(scenarios), 1);
upper_bound_market = zeros(length(scenarios), 1);
lower_bound_tariff = zeros(length(scenarios), 1);
upper_bound_tariff = zeros(length(scenarios), 1);

% Boucle sur chaque scénario pour calculer les revenus et les statistiques
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
    num_years = length(years);
    
    % Initialisation des revenus annuels
    revenue_market = zeros(num_years, 1);
    revenue_tariff = zeros(num_years, 1);
    
    for j = 1:num_years
        idx = data.year == years(j);
        revenue_market(j) = sum(data.dispatch(idx) .* data.base_price(idx)); % Somme annuelle
        revenue_tariff(j) = sum(data.dispatch(idx) .* data.tariff(idx)); % Somme annuelle
    end
    
    % Calcul des statistiques
    avg_revenue_market(i) = mean(revenue_market);
    avg_revenue_tariff(i) = mean(revenue_tariff);
    
    std_revenue_market(i) = std(revenue_market);
    std_revenue_tariff(i) = std(revenue_tariff);

    min_revenue_market(i) = min(revenue_market);
    max_revenue_market(i) = max(revenue_market);
    min_revenue_tariff(i) = min(revenue_tariff);
    max_revenue_tariff(i) = max(revenue_tariff);

    % Calcul des percentiles pour les barres d’erreur alternatives
    lower_bound_market(i) = prctile(revenue_market, 5);
    upper_bound_market(i) = prctile(revenue_market, 95);
    lower_bound_tariff(i) = prctile(revenue_tariff, 5);
    upper_bound_tariff(i) = prctile(revenue_tariff, 95);
end

% Création du bar chart avec barres d’erreur améliorées
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

% Ajout des barres d'erreur avec les percentiles
errorbar(xPos(1, :), avg_revenue_market, avg_revenue_market - lower_bound_market, upper_bound_market - avg_revenue_market, 'k.', 'LineWidth', 1.5);
errorbar(xPos(2, :), avg_revenue_tariff, avg_revenue_tariff - lower_bound_tariff, upper_bound_tariff - avg_revenue_tariff, 'k.', 'LineWidth', 1.5);

% Ajout des valeurs min et max sous forme de texte pour vérification
for i = 1:length(scenarios)
    text(xPos(1, i), max_revenue_market(i), sprintf('Max: %.1e', max_revenue_market(i)), 'FontSize', 10, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
    text(xPos(1, i), min_revenue_market(i), sprintf('Min: %.1e', min_revenue_market(i)), 'FontSize', 10, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top');
    
    text(xPos(2, i), max_revenue_tariff(i), sprintf('Max: %.1e', max_revenue_tariff(i)), 'FontSize', 10, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
    text(xPos(2, i), min_revenue_tariff(i), sprintf('Min: %.1e', min_revenue_tariff(i)), 'FontSize', 10, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top');
end

% Ajustement des étiquettes d'axe X
xticks(mean(xPos, 1));  
xticklabels(scenarios);

% Ajout des labels et du titre
ylabel('Average Revenue (€/y)');
legend('Market-based', 'Tariff-based', 'Location', 'best');
grid on;
hold off;

% Ajustement de la taille de la figure
set(gcf, 'Position', [100, 100, 900, 600]);
