clc; clear; close all;

DATA_PATH = fullfile(fileparts(mfilename('fullpath')), 'results', 'CSV');

selected_files = { 'storage_result_scenario_1.csv', ...
                   'storage_result_scenario_2.csv', ...
                   'storage_result_scenario_3.csv', ...
                   'storage_result_scenario_4.csv'};

scenarios = {'Without Tariff', 'Flat', 'Proportional', 'Piecewise'};

% Chargement des données
data = cell(length(selected_files), 1);
for i = 1:length(selected_files)
    filename = fullfile(DATA_PATH, selected_files{i});
    data{i} = readtable(filename);
end

% Nombre d'années disponibles dans les données
years = unique(data{1}.year);

% Initialisation de la figure pour le subplot
figure;

% Couleurs pour chaque scénario
colors = lines(length(scenarios));

% ---- Subplot 1 : Average Discharge (Pd) ----
subplot(2,1,1);
hold on;
for i = 1:length(scenarios)
    dispatch_data = [];
    for j = 1:length(years)
        subset = data{i}(data{i}.year == years(j), :);
        dispatch_data = [dispatch_data, mean(subset.Pd)]; % Moyenne du dispatch (décharge)
    end
    plot(years, dispatch_data, '-o', 'DisplayName', scenarios{i}, 'LineWidth', 2, 'Color', colors(i, :));
end
title('a');
xlabel('Year');
ylabel('Average Discharge (MW/h)');
legend('Location', 'best');
grid on;
hold off;

% ---- Subplot 2 : Average Charge (Pc) ----
subplot(2,1,2);
hold on;
for i = 1:length(scenarios)
    charge_data = [];
    for j = 1:length(years)
        subset = data{i}(data{i}.year == years(j), :);
        charge_data = [charge_data, mean(subset.Pc)]; % Moyenne de la charge (charge)
    end
    plot(years, charge_data, '-o', 'DisplayName', scenarios{i}, 'LineWidth', 2, 'Color', colors(i, :));
end
title('b');
xlabel('Year');
ylabel('Average Charge (MW/h)');
legend('Location', 'best');
grid on;
hold off;

% Ajustement de l'affichage
set(gcf, 'Position', [100, 100, 800, 600]); % Ajuste la taille de la figure
