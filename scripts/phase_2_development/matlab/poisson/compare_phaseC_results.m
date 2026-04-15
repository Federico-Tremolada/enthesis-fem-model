%% ===========================================================
% Script: compare_phaseC_results.m
% Author: FEDERICO TREMOLADA
%
% Purpose:
% Compare Phase C Abaqus results for models with constant and variable
% Poisson ratio by analyzing global summary metrics and line profiles.
%
% Models:
% - M17_PWR_n3_L16_nuConst_v1
% - M18_PWR_n3_L16_nuVar_v1
% - Any additional model structured in the same way
%
% Input:
% - summary_phaseC.csv
% - Line profile CSV files:
%     * M17_PWR_n3_L16_nuConst_v1_line.csv
%     * M18_PWR_n3_L16_nuVar_v1_line.csv
%
% Operations:
% - Read the summary table for Phase C
% - Sort models in the desired comparison order
% - Read line-profile CSV files
% - Average duplicated x positions when needed
% - Generate comparative S11(x) plots
% - Generate comparative von Mises(x) plots
% - Generate global peak comparison plots
% - Compare x and y positions of peak von Mises stress
% - Build a final comparison table
% - Compute simple percentage variations between the two models
%
% Output:
% - phaseC_figures/phaseC_S11_profiles.png
% - phaseC_figures/phaseC_Mises_profiles.png
% - phaseC_figures/phaseC_global_peaks.png
% - phaseC_figures/phaseC_peak_position.png
% - phaseC_figures/phaseC_final_table.csv
%
% Notes:
% - This script is intended for standard MATLAB post-processing
% - Update the dataFolder variable according to your own project structure
% - The script assumes that all required CSV files are stored in the
%   selected working directory or in the specified folder
%% ===========================================================

clear; clc; close all;

%% === USER SETTINGS ===

% Folder containing the CSV files.
% Update this path according to your local project structure.
dataFolder = fullfile(pwd, 'results_folder');

summaryFile = fullfile(dataFolder, 'summary_phaseC.csv');

lineFiles = {
    'M17_PWR_n3_L16_nuConst_v1_line.csv'
    'M18_PWR_n3_L16_nuVar_v1_line.csv'
};

modelLabels = {
    '\nu costante'
    '\nu variabile'
};

outFolder = fullfile(dataFolder, 'phaseC_figures');
if ~exist(outFolder, 'dir')
    mkdir(outFolder);
end

%% === READ SUMMARY ===

summaryTbl = readtable(summaryFile);

disp('=== SUMMARY TABLE ===');
disp(summaryTbl);

%% === SORT IN DESIRED ORDER ===

desiredOrder = {
    'M17_PWR_n3_L16_nuConst_v1'
    'M18_PWR_n3_L16_nuVar_v1'
};

[~, idxOrder] = ismember(desiredOrder, summaryTbl.model_name);
summaryTbl = summaryTbl(idxOrder, :);

%% === READ LINE FILES ===

lineTables = cell(numel(lineFiles),1);

for i = 1:numel(lineFiles)
    T = readtable(fullfile(dataFolder, lineFiles{i}));

    % If there are two rows for each x position near the centerline,
    % average values by x
    [xUnique, ~, ic] = unique(T.x);
    s11Mean = accumarray(ic, T.S11, [], @mean);
    misesMean = accumarray(ic, T.Mises, [], @mean);

    Tmean = table(xUnique, s11Mean, misesMean, ...
        'VariableNames', {'x','S11','Mises'});

    lineTables{i} = Tmean;
end

%% === PLOT 1: S11(x) ===

figure('Color','w');
hold on; grid on; box on;

for i = 1:numel(lineTables)
    plot(lineTables{i}.x, lineTables{i}.S11, 'LineWidth', 2, ...
        'DisplayName', modelLabels{i});
end

xlabel('x [mm]');
ylabel('S11 [MPa]');
title('Phase C - Comparison of S11(x) profiles');
legend('Location','best');
set(gca, 'FontSize', 11);

saveas(gcf, fullfile(outFolder, 'phaseC_S11_profiles.png'));

%% === PLOT 2: von Mises(x) ===

figure('Color','w');
hold on; grid on; box on;

for i = 1:numel(lineTables)
    plot(lineTables{i}.x, lineTables{i}.Mises, 'LineWidth', 2, ...
        'DisplayName', modelLabels{i});
end

xlabel('x [mm]');
ylabel('von Mises [MPa]');
title('Phase C - Comparison of von Mises(x) profiles');
legend('Location','best');
set(gca, 'FontSize', 11);

saveas(gcf, fullfile(outFolder, 'phaseC_Mises_profiles.png'));

%% === PLOT 3: global peaks ===

figure('Color','w');

tiledlayout(1,3, 'Padding','compact', 'TileSpacing','compact');

nexttile;
bar(summaryTbl.max_mises);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 10);
ylabel('max von Mises [MPa]');
title('Global max von Mises');
grid on; box on;

nexttile;
bar(summaryTbl.min_s11);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 10);
ylabel('min S11 [MPa]');
title('Global min S11');
grid on; box on;

nexttile;
bar(summaryTbl.max_s11);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 10);
ylabel('max S11 [MPa]');
title('Global max S11');
grid on; box on;

saveas(gcf, fullfile(outFolder, 'phaseC_global_peaks.png'));

%% === PLOT 4: peak position comparison ===

figure('Color','w');

tiledlayout(1,2, 'Padding','compact', 'TileSpacing','compact');

nexttile;
plot(1:height(summaryTbl), summaryTbl.max_mises_x, '-o', 'LineWidth', 2, 'MarkerSize', 7);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 11);
ylabel('x position of von Mises peak [mm]');
title('x position of von Mises peak');
grid on; box on;

nexttile;
plot(1:height(summaryTbl), summaryTbl.max_mises_y, '-o', 'LineWidth', 2, 'MarkerSize', 7);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 11);
ylabel('y position of von Mises peak [mm]');
title('y position of von Mises peak');
grid on; box on;

saveas(gcf, fullfile(outFolder, 'phaseC_peak_position.png'));

%% === FINAL TABLE ===

finalTbl = table;
finalTbl.Model = modelLabels;
finalTbl.MaxMises = summaryTbl.max_mises;
finalTbl.MaxMises_X = summaryTbl.max_mises_x;
finalTbl.MaxMises_Y = summaryTbl.max_mises_y;
finalTbl.MaxS11 = summaryTbl.max_s11;
finalTbl.MaxS11_X = summaryTbl.max_s11_x;
finalTbl.MaxS11_Y = summaryTbl.max_s11_y;
finalTbl.MinS11 = summaryTbl.min_s11;
finalTbl.MinS11_X = summaryTbl.min_s11_x;
finalTbl.MinS11_Y = summaryTbl.min_s11_y;

writetable(finalTbl, fullfile(outFolder, 'phaseC_final_table.csv'));

disp('=== FINAL TABLE ===');
disp(finalTbl);

%% === SIMPLE AUTOMATIC COMMENT ===

deltaMises = 100 * (summaryTbl.max_mises(2) - summaryTbl.max_mises(1)) / summaryTbl.max_mises(1);
deltaMinS11 = 100 * (abs(summaryTbl.min_s11(2)) - abs(summaryTbl.min_s11(1))) / abs(summaryTbl.min_s11(1));

fprintf('\n');
fprintf('Variation in max von Mises (\x03bd variable vs constant): %+0.2f %%\n', deltaMises);
fprintf('Variation in |min S11| (\x03bd variable vs constant): %+0.2f %%\n', deltaMinS11);
fprintf('\nFigures saved in:\n%s\n', outFolder);
