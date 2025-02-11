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
    Pd = data.Pd;  
    price = data.price;  
    net_load = data.net_load; 
    revenue = Pd .* price;  % Calcul du revenu (Pd * price)
    
    % Trier les données pour un tracé lissé
    [net_load_sorted, idx] = sort(net_load); 
    revenue_sorted = revenue(idx);
    
    % Appliquer un lissage avec movmean (moyenne glissante)
    window_size = round(length(revenue_sorted) * 0.05);  % Fenêtre de 5% des données
    revenue_smoothed = movmean(revenue_sorted, window_size);
    
    % Création du subplot
    subplot(2, 2, i);
    hold on;
    
    % Tracé des courbes lissées
    plot(net_load_sorted, revenue_smoothed, 'Color', colors(i, :), 'LineWidth', 2);
    
    % Personnalisation des axes et des titres
    xlabel('Charge Nette (net\_load)');
    ylabel('Revenu (Pd * Price)');
    title(['Revenu vs Net Load - ' scenarios{i}]);
    grid on;
    
    % Ajouter une légende
    legend(scenarios{i}, 'Location', 'best');
    
    hold off;
end

% Ajouter un titre global
sgtitle('Évolution du Revenu (Pd * Price) en fonction de la Charge Nette');

% Ajustement de l'affichage
set(gcf, 'Position', [100, 100, 1000, 600]); % Ajuster la taille de la figure
