%% ===========================================================
% Script: postprocess_enthesis.m
% Author: FEDERICO TREMOLADA
%
% Purpose:
% Perform post-processing of FEM results obtained from Abaqus
% simulations by comparing S11 stress profiles along the
% tendon-bone interface.
%
% Models:
% - M01_sharp_v1
% - M02_linear_v1
% - M03_exponential_v1
% - M04_power_n05_v1
% - M05_power_n2_v1
% - Any additional model structured in the same way
%
% Input:
% - CSV files containing:
%     x   -> coordinate along the interface [mm]
%     S11 -> longitudinal stress [MPa]
%
% Operations:
% - Read CSV files containing S11(x) stress profiles
% - Compare multiple models (sharp, graded, power-law)
% - Interpolate data onto a common spatial grid
% - Generate comparative plots
% - Compute key quantitative metrics
%
% Output:
% - Comparative S11(x) plot
% - Key metrics:
%     * maximum/minimum S11
%     * peak locations
%     * S11 value at the interface
% - Automatically saved files:
%     * summary_metrics.csv
%     * S11_comparison.png
%     * metrics_barplot.png
%
% Notes:
% - The script is robust to:
%     * column name variations (case-insensitive)
%     * unordered data
%     * presence of NaN values
% - Update file names according to your own project structure
% - This script uses folder selection through a dialog window
%% ===========================================================

clear; close all; clc;

%% =========================
% 1. CSV FOLDER SELECTION
%% =========================

folder = uigetdir(pwd, 'Select the folder containing the CSV files');

if isequal(folder, 0)
    error('No folder selected. Script interrupted.');
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
        error('File not found: %s', file_path);
    end
    
    T = readtable(file_path);
    vars = T.Properties.VariableNames;
    vars_lower = lower(vars);
    
    % Search x column (case-insensitive)
    idx_x = find(strcmp(vars_lower, 'x'), 1);
    
    % Search S11 column (case-insensitive)
    idx_s11 = find(strcmp(vars_lower, 's11'), 1);
    
    if isempty(idx_x)
        error('In file %s, no column named x/X was found.', files{i});
    end
    
    if isempty(idx_s11)
        error('In file %s, no column named S11/s11 was found.', files{i});
    end
    
    x = T.(vars{idx_x});
    S11 = T.(vars{idx_s11});
    
    % Convert to column vectors
    x = x(:);
    S11 = S11(:);
    
    % Numeric check
    if ~isnumeric(x) || ~isnumeric(S11)
        error('Columns x and S11 in file %s must be numeric.', files{i});
    end
    
    % Remove NaN values
    valid = ~(isnan(x) | isnan(S11));
    x = x(valid);
    S11 = S11(valid);
    
    if isempty(x)
        error('After NaN removal, file %s contains no valid data.', files{i});
    end
    
    % Sort by x
    [x, idx_sort] = sort(x);
    S11 = S11(idx_sort);
    
    % Remove duplicated x values
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
    error('Invalid common x range. Check the CSV files.');
end

x_common = linspace(x_min, x_max, 300)';
S11_interp = zeros(length(x_common), n_models);

for i = 1:n_models
    S11_interp(:,i) = interp1(data{i}.x, data{i}.S11, x_common, 'linear');
end

%% =========================
% 5. MAIN PLOT
%% =========================

fig1 = figure('Name','S11 comparison vs x','Color','w');
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
title('Model comparison: S11 along the interface line');

x_interface = 15;
xline(x_interface, '--k', 'Interface', ...
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
fprintf('       MODEL METRICS\n');
fprintf('==============================\n');

for i = 1:n_models
    fprintf('\nModel: %s\n', metrics(i).name);
    fprintf('  Max S11           = %.4f MPa\n', metrics(i).Smax);
    fprintf('  Min S11           = %.4f MPa\n', metrics(i).Smin);
    fprintf('  Max S11 position  = %.4f mm\n', metrics(i).x_max);
    fprintf('  Min S11 position  = %.4f mm\n', metrics(i).x_min);
    fprintf('  S11 @ interface   = %.4f MPa\n', metrics(i).S_interface);
end

%% =========================
% 8. SUMMARY TABLE
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
disp('Summary table:');
disp(ResultsTable);

%% =========================
% 9. BAR PLOT METRICS
%% =========================

fig2 = figure('Name','Synthetic metrics','Color','w');

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
title('S11 at the interface');
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

fprintf('\nFiles saved in the selected folder:\n');
fprintf('  - summary_metrics.csv\n');
fprintf('  - S11_comparison.png\n');
fprintf('  - metrics_barplot.png\n');
