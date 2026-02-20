clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV/100/germany');

selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

scenarios = {'scenario_1', 'scenario_2', 'scenario_3', 'scenario_4'};
colors = lines(length(scenarios));

% Chargement des données
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Calcul de l'amplitude du dispatch par tarif pour chaque scénario
dispatch_amplitude = zeros(length(scenarios), 1);
mean_dispatch = zeros(length(scenarios), 1);

for i = 1:length(data)
    % Calcul de l'amplitude du dispatch pour chaque année (si plusieurs années sont présentes)
    dispatch_diff = data{i}.Pd - data{i}.Pc; % Amplitude du dispatch
    dispatch_amplitude(i) = max(dispatch_diff) - min(dispatch_diff); % Amplitude totale
    mean_dispatch(i) = mean(dispatch_diff); % Moyenne du dispatch
end

% Comparaison de l'amplitude du dispatch par tarif
figure;
bar(dispatch_amplitude, 'FaceColor', 'flat');
set(gca, 'XTickLabel', scenarios);
xlabel('Scénarios');
ylabel('Amplitude du Dispatch');
title('Amplitude du Dispatch pour chaque Tarif');
grid on;

% Comparaison de la moyenne du dispatch par tarif
figure;
bar(mean_dispatch, 'FaceColor', 'flat');
set(gca, 'XTickLabel', scenarios);
xlabel('Scénarios');
ylabel('Moyenne du Dispatch');
title('Moyenne du Dispatch par Tarif');
grid on;

% Graphique de l'influence du tarif sur l'amplitude du dispatch
% Pour éviter les graphiques flous, nous utilisons un sous-ensemble de données
year_to_plot = 2020;  % Modifier selon l'analyse
figure;
hold on;
for i = 1:length(data)
    subset = data{i}(data{i}.year == year_to_plot, :);
    scatter(subset.tariff, subset.Pd - subset.Pc, 30, colors(i, :), 'filled');
end
legend(scenarios, 'Location', 'best');
xlabel('Tarif');
ylabel('Dispatch (Pd - Pc)');
title(['Impact du Tarif sur le Dispatch (Année ', num2str(year_to_plot), ')']);
grid on;
hold off;

% Histogramme des amplitudes du dispatch pour chaque scénario
figure;
hold on;
for i = 1:length(data)
    dispatch_diff = data{i}.Pd - data{i}.Pc;
    histogram(dispatch_diff, 'FaceColor', colors(i, :), 'DisplayName', scenarios{i}, 'BinWidth', 2);
end
legend('show');
xlabel('Amplitude du Dispatch');
ylabel('Fréquence');
title('Distribution de l''Amplitude du Dispatch par Scénario');
grid on;
hold off;
