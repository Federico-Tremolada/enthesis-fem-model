clear; close all; clc;

%% =========================
% 1. SELEZIONE CARTELLA CSV
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
% 3. LETTURA DATI ROBUSTA
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
    
    idx_x = find(strcmp(vars_lower, 'x'), 1);
    idx_s11 = find(strcmp(vars_lower, 's11'), 1);
    
    if isempty(idx_x)
        error('Nel file %s non trovo una colonna chiamata x/X.', files{i});
    end
    
    if isempty(idx_s11)
        error('Nel file %s non trovo una colonna chiamata S11/s11.', files{i});
    end
    
    x = T.(vars{idx_x});
    S11 = T.(vars{idx_s11});
    
    x = x(:);
    S11 = S11(:);
    
    if ~isnumeric(x) || ~isnumeric(S11)
        error('Le colonne x e S11 nel file %s devono essere numeriche.', files{i});
    end
    
    valid = ~(isnan(x) | isnan(S11));
    x = x(valid);
    S11 = S11(valid);
    
    if isempty(x)
        error('Il file %s non contiene dati validi.', files{i});
    end
    
    [x, idx_sort] = sort(x);
    S11 = S11(idx_sort);
    
    [x_unique, idx_unique] = unique(x, 'stable');
    S11_unique = S11(idx_unique);
    
    data{i}.x = x_unique;
    data{i}.S11 = S11_unique;
end

%% =========================
% 4. INTERPOLAZIONE SU GRIGLIA COMUNE
%% =========================

x_min = max(cellfun(@(d) min(d.x), data));
x_max = min(cellfun(@(d) max(d.x), data));

if x_min >= x_max
    error('Intervallo comune in x non valido. Controlla i CSV.');
end

n_points = 500;
x_common = linspace(x_min, x_max, n_points)';
dx = mean(diff(x_common));

S11_interp = zeros(length(x_common), n_models);

for i = 1:n_models
    S11_interp(:,i) = interp1(data{i}.x, data{i}.S11, x_common, 'linear');
end

%% =========================
% 5. GRAFICO PRINCIPALE
%% =========================

fig1 = figure('Name','Confronto S11 vs x','Color','w');
hold on; grid on; box on;

colors = lines(n_models);

for i = 1:n_models
    plot(x_common, S11_interp(:,i), ...
        'LineWidth', 2.2, ...
        'Color', colors(i,:));
end

x_interface = 15;
xline(x_interface, '--k', 'Interfaccia', ...
    'LineWidth', 1.5, ...
    'LabelVerticalAlignment', 'middle');

xlabel('x [mm]');
ylabel('S11 [MPa]');
title('Confronto dei modelli: S11 lungo la linea');
legend(model_names, 'Location', 'best');
set(gca, 'FontSize', 12);

%% =========================
% 6. CALCOLO METRICHE AVANZATE
%% =========================

metrics = struct();

S_sharp = S11_interp(:,1); % riferimento

for i = 1:n_models
    
    S = S11_interp(:,i);
    
    % Derivata prima e seconda
    dSdx = gradient(S, x_common);
    d2Sdx2 = gradient(dSdx, x_common);
    
    % Massimi/minimi
    [Smax, idx_max] = max(S);
    [Smin, idx_min] = min(S);
    
    x_max_pos = x_common(idx_max);
    x_min_pos = x_common(idx_min);
    
    % Valore all'interfaccia
    S_interface = interp1(x_common, S, x_interface, 'linear');
    
    % Range
    S_range = Smax - Smin;
    
    % Smoothness metrics
    max_abs_gradient = max(abs(dSdx));
    mean_abs_gradient = mean(abs(dSdx));
    mean_abs_curvature = mean(abs(d2Sdx2));
    max_abs_curvature = max(abs(d2Sdx2));
    
    % Area differenza rispetto a Sharp
    area_vs_sharp = trapz(x_common, abs(S - S_sharp));
    
    % Area assoluta della curva
    area_abs_S11 = trapz(x_common, abs(S));
    
    metrics(i).name = model_names{i};
    metrics(i).Smax = Smax;
    metrics(i).Smin = Smin;
    metrics(i).x_max = x_max_pos;
    metrics(i).x_min = x_min_pos;
    metrics(i).S_interface = S_interface;
    metrics(i).S_range = S_range;
    metrics(i).max_abs_gradient = max_abs_gradient;
    metrics(i).mean_abs_gradient = mean_abs_gradient;
    metrics(i).mean_abs_curvature = mean_abs_curvature;
    metrics(i).max_abs_curvature = max_abs_curvature;
    metrics(i).area_vs_sharp = area_vs_sharp;
    metrics(i).area_abs_S11 = area_abs_S11;
end

%% =========================
% 7. TABELLA COMPLETA
%% =========================

ResultsTable = table( ...
    string({metrics.name})', ...
    [metrics.Smax]', ...
    [metrics.Smin]', ...
    [metrics.x_max]', ...
    [metrics.x_min]', ...
    [metrics.S_interface]', ...
    [metrics.S_range]', ...
    [metrics.max_abs_gradient]', ...
    [metrics.mean_abs_gradient]', ...
    [metrics.mean_abs_curvature]', ...
    [metrics.max_abs_curvature]', ...
    [metrics.area_vs_sharp]', ...
    [metrics.area_abs_S11]', ...
    'VariableNames', { ...
    'Model', ...
    'Max_S11_MPa', ...
    'Min_S11_MPa', ...
    'X_Max_mm', ...
    'X_Min_mm', ...
    'S11_Interface_MPa', ...
    'S11_Range_MPa', ...
    'MaxAbs_dSdx', ...
    'MeanAbs_dSdx', ...
    'MeanAbs_d2Sdx2', ...
    'MaxAbs_d2Sdx2', ...
    'Area_vs_Sharp', ...
    'AreaAbs_S11'});

disp(' ');
disp('==============================');
disp('     TABELLA COMPLETA');
disp('==============================');
disp(ResultsTable);

%% =========================
% 8. STAMPA INTERPRETATIVA
%% =========================

fprintf('\n==============================\n');
fprintf('   INTERPRETAZIONE NUMERICA\n');
fprintf('==============================\n');

[~, idx_best_grad] = min([metrics.max_abs_gradient]);
[~, idx_best_curv] = min([metrics.mean_abs_curvature]);
[~, idx_best_interface] = max([metrics.S_interface]); 
% max perché sono valori negativi: meno negativo = migliore

fprintf('\nModello con gradiente massimo minore: %s\n', metrics(idx_best_grad).name);
fprintf('  max|dS/dx| = %.4f\n', metrics(idx_best_grad).max_abs_gradient);

fprintf('\nModello con curvatura media minore: %s\n', metrics(idx_best_curv).name);
fprintf('  mean|d2S/dx2| = %.4f\n', metrics(idx_best_curv).mean_abs_curvature);

fprintf('\nModello con S11 all''interfaccia meno severo: %s\n', metrics(idx_best_interface).name);
fprintf('  S11_interface = %.4f MPa\n', metrics(idx_best_interface).S_interface);

%% =========================
% 9. GRAFICO DERIVATA PRIMA
%% =========================

fig2 = figure('Name','Gradiente di stress','Color','w');
hold on; grid on; box on;

for i = 1:n_models
    dSdx = gradient(S11_interp(:,i), x_common);
    plot(x_common, dSdx, 'LineWidth', 2, 'Color', colors(i,:));
end

xline(x_interface, '--k', 'Interfaccia', 'LineWidth', 1.5);
xlabel('x [mm]');
ylabel('dS11/dx [MPa/mm]');
title('Gradiente di stress lungo la linea');
legend(model_names, 'Location', 'best');
set(gca, 'FontSize', 12);

%% =========================
% 10. GRAFICO CURVATURA
%% =========================

fig3 = figure('Name','Curvatura di stress','Color','w');
hold on; grid on; box on;

for i = 1:n_models
    dSdx = gradient(S11_interp(:,i), x_common);
    d2Sdx2 = gradient(dSdx, x_common);
    plot(x_common, d2Sdx2, 'LineWidth', 2, 'Color', colors(i,:));
end

xline(x_interface, '--k', 'Interfaccia', 'LineWidth', 1.5);
xlabel('x [mm]');
ylabel('d^2S11/dx^2 [MPa/mm^2]');
title('Curvatura del campo di stress');
legend(model_names, 'Location', 'best');
set(gca, 'FontSize', 12);

%% =========================
% 11. BARPLOT METRICHE CHIAVE
%% =========================

fig4 = figure('Name','Metriche chiave','Color','w');

subplot(2,2,1);
bar([metrics.S_interface]');
title('S11 all''interfaccia');
ylabel('MPa');
set(gca, 'XTick', 1:n_models, 'XTickLabel', model_names);
xtickangle(30); grid on; box on;

subplot(2,2,2);
bar([metrics.max_abs_gradient]');
title('max |dS11/dx|');
ylabel('MPa/mm');
set(gca, 'XTick', 1:n_models, 'XTickLabel', model_names);
xtickangle(30); grid on; box on;

subplot(2,2,3);
bar([metrics.mean_abs_curvature]');
title('mean |d^2S11/dx^2|');
ylabel('MPa/mm^2');
set(gca, 'XTick', 1:n_models, 'XTickLabel', model_names);
xtickangle(30); grid on; box on;

subplot(2,2,4);
bar([metrics.area_vs_sharp]');
title('Area differenza vs Sharp');
ylabel('MPa·mm');
set(gca, 'XTick', 1:n_models, 'XTickLabel', model_names);
xtickangle(30); grid on; box on;

%% =========================
% 12. RANKING FINALE
%% =========================
% Ranking basato su:
% - S11_interface (meno severo = meglio)
% - max_abs_gradient (minore = meglio)
% - mean_abs_curvature (minore = meglio)

S_interface_vals = [metrics.S_interface]';
grad_vals        = [metrics.max_abs_gradient]';
curv_vals        = [metrics.mean_abs_curvature]';

model_col = string({metrics.name})';

% normalizzazione 0-1
% per S11_interface: valori meno negativi sono migliori
score_interface = (S_interface_vals - min(S_interface_vals)) ./ ...
                  (max(S_interface_vals) - min(S_interface_vals) + eps);

% per gradiente e curvatura: più piccolo = migliore
score_grad = 1 - (grad_vals - min(grad_vals)) ./ ...
                 (max(grad_vals) - min(grad_vals) + eps);

score_curv = 1 - (curv_vals - min(curv_vals)) ./ ...
                 (max(curv_vals) - min(curv_vals) + eps);

final_score = (score_interface + score_grad + score_curv) / 3;

RankingTable = table( ...
    model_col, ...
    score_interface, ...
    score_grad, ...
    score_curv, ...
    final_score, ...
    'VariableNames', {'Model','Score_Interface','Score_Gradient','Score_Curvature','Final_Score'});

RankingTable = sortrows(RankingTable, 'Final_Score', 'descend');

disp(' ');
disp('==============================');
disp('       RANKING FINALE');
disp('==============================');
disp(RankingTable);

%% =========================
% 13. SALVATAGGIO OUTPUT
%% =========================

writetable(ResultsTable, fullfile(folder, 'summary_metrics_advanced.csv'));
writetable(RankingTable, fullfile(folder, 'model_ranking.csv'));

exportgraphics(fig1, fullfile(folder, 'S11_comparison_advanced.png'), 'Resolution', 300);
exportgraphics(fig2, fullfile(folder, 'stress_gradient_comparison.png'), 'Resolution', 300);
exportgraphics(fig3, fullfile(folder, 'stress_curvature_comparison.png'), 'Resolution', 300);
exportgraphics(fig4, fullfile(folder, 'advanced_metrics_barplot.png'), 'Resolution', 300);

fprintf('\nFile salvati nella cartella selezionata:\n');
fprintf('  - summary_metrics_advanced.csv\n');
fprintf('  - model_ranking.csv\n');
fprintf('  - S11_comparison_advanced.png\n');
fprintf('  - stress_gradient_comparison.png\n');
fprintf('  - stress_curvature_comparison.png\n');
fprintf('  - advanced_metrics_barplot.png\n');