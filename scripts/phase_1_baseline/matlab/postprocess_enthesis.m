%% ===========================================================
% FEM POST-PROCESSING — S11 ANALYSIS ALONG THE INTERFACE
% ============================================================
%
% Description:
% This script performs post-processing of FEM results obtained
% from Abaqus simulations of different enthesis models.
%
% Specifically, it:
% - Reads CSV files containing S11(x) stress profiles
% - Compares multiple models (sharp, graded, power-law)
% - Interpolates data onto a common spatial grid
% - Generates comparative plots
% - Computes key quantitative metrics
%
% Engineering objective:
% Evaluate the effect of material grading on the stress
% distribution along the tendon-bone interface.
%
% Input:
% - CSV files containing:
%     x   → coordinate along the interface [mm]
%     S11 → longitudinal stress [MPa]
%
% Output:
% - Comparative S11(x) plot
% - Key metrics:
%     • maximum/minimum S11
%     • peak locations
%     • S11 value at the interface
% - Automatically saved files:
%     • summary_metrics.csv
%     • S11_comparison.png
%     • metrics_barplot.png
%
% Notes:
% - The script is robust to:
%     • column name variations (case-insensitive)
%     • unordered data
%     • presence of NaN values
%
% Author: FEDERICO TREMOLADA
% Project: Entesis FEM Study
% ============================================================

clear; close all; clc;

%% =========================
% 1. CSV FOLDER SELECTION
%% =========================

folder = uigetdir(pwd, 'Seleziona la cartella contenente i file CSV');

if isequal(folder, 0)
    error('Nessuna cartella selezionata. Script interrotto.');
end

%% =========================
% 2. FILE INPUT
%% =========================

files = {
    'M01_sharp_v1_line.csv'
    'M02_linear_v1_line.csv'
    'M03_exponential_v1_line.csv'
    'M04_power_n05_v1_line.csv'
    'M05_power_n2_v1_line.csv'
};

model_names = {
    'Sharp'
    'Linear'
    'Exponential'
    'Power n=0.5'
    'Power n=2'
};

n_models = numel(files);

%% =========================
% 3. DATA READING
%% =========================

data = cell(n_models,1);

for i = 1:n_models
    
    file_path = fullfile(folder, files{i});
    
    if ~isfile(file_path)
        error('File non trovato: %s', file_path);
    end
    
    T = readtable(file_path);
    vars = T.Properties.VariableNames;
    vars_lower = lower(vars);
    
    % Cerca colonna x (case-insensitive)
    idx_x = find(strcmp(vars_lower, 'x'), 1);
    
    % Cerca colonna S11 (case-insensitive)
    idx_s11 = find(strcmp(vars_lower, 's11'), 1);
    
    if isempty(idx_x)
        error('Nel file %s non trovo una colonna chiamata x/X.', files{i});
    end
    
    if isempty(idx_s11)
        error('Nel file %s non trovo una colonna chiamata S11/s11.', files{i});
    end
    
    x = T.(vars{idx_x});
    S11 = T.(vars{idx_s11});
    
    % Converte in vettori colonna
    x = x(:);
    S11 = S11(:);
    
    % Controllo numerico
    if ~isnumeric(x) || ~isnumeric(S11)
        error('Le colonne x e S11 nel file %s devono essere numeriche.', files{i});
    end
    
    % Rimuove eventuali NaN
    valid = ~(isnan(x) | isnan(S11));
    x = x(valid);
    S11 = S11(valid);
    
    if isempty(x)
        error('Dopo la rimozione dei NaN, il file %s non contiene dati validi.', files{i});
    end
    
    % Ordina per x
    [x, idx_sort] = sort(x);
    S11 = S11(idx_sort);
    
    % Rimuove eventuali duplicati in x
    [x_unique, idx_unique] = unique(x, 'stable');
    S11_unique = S11(idx_unique);
    
    data{i}.x = x_unique;
    data{i}.S11 = S11_unique;
end

%% =========================
% 4. INTERPOLATION ON COMMON GRID
%% =========================

x_min = max(cellfun(@(d) min(d.x), data));
x_max = min(cellfun(@(d) max(d.x), data));

if x_min >= x_max
    error('Intervallo comune in x non valido. Controlla i CSV.');
end

x_common = linspace(x_min, x_max, 300)';
S11_interp = zeros(length(x_common), n_models);

for i = 1:n_models
    S11_interp(:,i) = interp1(data{i}.x, data{i}.S11, x_common, 'linear');
end

%% =========================
% 5. MAIN PLOT
%% =========================

fig1 = figure('Name','Confronto S11 vs x','Color','w');
hold on;
grid on;
box on;

colors = lines(n_models);

for i = 1:n_models
    plot(x_common, S11_interp(:,i), ...
        'LineWidth', 2, ...
        'Color', colors(i,:));
end

xlabel('x [mm]');
ylabel('S11 [MPa]');
title('Confronto dei modelli: S11 lungo la linea');

x_interface = 15;
xline(x_interface, '--k', 'Interfaccia', ...
    'LineWidth', 1.5, ...
    'LabelVerticalAlignment', 'middle');

legend(model_names, 'Location', 'best');
set(gca, 'FontSize', 12);

%% =========================
% 6. METRICS
%% =========================

metrics = struct();

for i = 1:n_models
    
    S = S11_interp(:,i);
    
    [Smax, idx_max] = max(S);
    [Smin, idx_min] = min(S);
    
    x_max_pos = x_common(idx_max);
    x_min_pos = x_common(idx_min);
    
    S_interface = interp1(x_common, S, x_interface, 'linear');
    
    metrics(i).name = model_names{i};
    metrics(i).Smax = Smax;
    metrics(i).Smin = Smin;
    metrics(i).x_max = x_max_pos;
    metrics(i).x_min = x_min_pos;
    metrics(i).S_interface = S_interface;
end

%% =========================
% 7. RESULTS PRINTING 
%% =========================

fprintf('\n==============================\n');
fprintf('       METRICHE MODELLO\n');
fprintf('==============================\n');

for i = 1:n_models
    fprintf('\nModel: %s\n', metrics(i).name);
    fprintf('  Max S11           = %.4f MPa\n', metrics(i).Smax);
    fprintf('  Min S11           = %.4f MPa\n', metrics(i).Smin);
    fprintf('  Posizione max S11 = %.4f mm\n', metrics(i).x_max);
    fprintf('  Posizione min S11 = %.4f mm\n', metrics(i).x_min);
    fprintf('  S11 @ interfaccia = %.4f MPa\n', metrics(i).S_interface);
end

%% =========================
% 8. SUM-UP CHART
%% =========================

ResultsTable = table( ...
    string({metrics.name})', ...
    [metrics.Smax]', ...
    [metrics.Smin]', ...
    [metrics.x_max]', ...
    [metrics.x_min]', ...
    [metrics.S_interface]', ...
    'VariableNames', {'Model','Max_S11_MPa','Min_S11_MPa','X_Max_mm','X_Min_mm','S11_Interface_MPa'});

disp(' ');
disp('Tabella riassuntiva:');
disp(ResultsTable);

%% =========================
% 9. BAR PLOT METRICS
%% =========================

fig2 = figure('Name','Metriche sintetiche','Color','w');

subplot(1,2,1);
bar([metrics.Smax]');
title('Max S11');
ylabel('S11 [MPa]');
set(gca, 'XTick', 1:n_models, 'XTickLabel', model_names, 'FontSize', 11);
xtickangle(30);
grid on;
box on;

subplot(1,2,2);
bar([metrics.S_interface]');
title('S11 all''interfaccia');
ylabel('S11 [MPa]');
set(gca, 'XTick', 1:n_models, 'XTickLabel', model_names, 'FontSize', 11);
xtickangle(30);
grid on;
box on;

%% =========================
% 10. OUTPUT SAVING
%% =========================

writetable(ResultsTable, fullfile(folder, 'summary_metrics.csv'));
exportgraphics(fig1, fullfile(folder, 'S11_comparison.png'), 'Resolution', 300);
exportgraphics(fig2, fullfile(folder, 'metrics_barplot.png'), 'Resolution', 300);

fprintf('\nFile salvati nella cartella selezionata:\n');
fprintf('  - summary_metrics.csv\n');
fprintf('  - S11_comparison.png\n');
fprintf('  - metrics_barplot.png\n');
