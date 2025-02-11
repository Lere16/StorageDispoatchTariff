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
colors = lines(10); % Palette de couleurs pour plus de 4 courbes

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
    
    % Extraction des années uniques
    years = unique(data.year);
    
    % Création du subplot
    subplot(2, 2, i);
    hold on;
    
    % Boucle pour chaque année
    for j = 1:length(years)
        % Filtrer les données par année
        year_data = data(data.year == years(j), :);
        net_load_year = year_data.net_load;
        revenue_year = year_data.Pd .* year_data.price;
        
        % Trier les données pour l'année spécifique
        [net_load_sorted_year, idx_year] = sort(net_load_year); 
        revenue_sorted_year = revenue_year(idx_year);
        
        % Appliquer un lissage sur les données de l'année
        revenue_smoothed_year = movmean(revenue_sorted_year, window_size);
        
        % Tracer la courbe pour cette année
        plot(net_load_sorted_year, revenue_smoothed_year, 'Color', colors(j, :), 'LineWidth', 2);
    end % Fin de la boucle sur les années
    
    % Personnalisation des axes et des titres
    xlabel('Charge Nette (net\_load)');
    ylabel('Revenu (Pd * Price)');
    title(['Revenu vs Net Load - ' scenarios{i}]);
    grid on;
    
    % Ajouter une légende pour les années
    legend(string(years), 'Location', 'best');
    
    hold off;
end % Fin de la boucle sur les scénarios

% Ajouter un titre global
sgtitle('Évolution du Revenu (Pd * Price) en fonction de la Charge Nette');

% Ajustement de l'affichage
set(gcf, 'Position', [100, 100, 1000, 600]); % Ajuster la taille de la figure
