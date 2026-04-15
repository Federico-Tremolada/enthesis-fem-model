%% ===========================================================
% Script: compare_phaseB_results.m
% Author: FEDERICO TREMOLADA
%
% Purpose:
% Compare Phase B power-law sensitivity results by analyzing global
% summary metrics and line profiles for different exponent values.
%
% Models:
% - M13_PWR_n1p5_L16_v1
% - M14_PWR_n2_L16_v1
% - M15_PWR_n3_L16_v1
% - M16_PWR_n5_L16_v1
% - Any additional model structured in the same way
%
% Input:
% - summary_phaseB.csv
% - Line profile CSV files:
%     * M13_PWR_n1p5_L16_v1_line.csv
%     * M14_PWR_n2_L16_v1_line.csv
%     * M15_PWR_n3_L16_v1_line.csv
%     * M16_PWR_n5_L16_v1_line.csv
%
% Operations:
% - Read the summary table for Phase B
% - Sort models in the desired comparison order
% - Read line-profile CSV files
% - Average duplicated x positions when needed
% - Generate comparative S11(x) plots
% - Generate comparative von Mises(x) plots
% - Generate global peak comparison plots
% - Track the shift of peak von Mises position
% - Build a final decision table
% - Provide a simple automatic indication of the best candidate model
%
% Output:
% - phaseB_figures/phaseB_S11_profiles.png
% - phaseB_figures/phaseB_Mises_profiles.png
% - phaseB_figures/phaseB_global_peaks.png
% - phaseB_figures/phaseB_peak_position.png
% - phaseB_figures/phaseB_final_table.csv
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

% Summary file
summaryFile = fullfile(dataFolder, 'summary_phaseB.csv');

% Line profile files
lineFiles = {
    'M13_PWR_n1p5_L16_v1_line.csv'
    'M14_PWR_n2_L16_v1_line.csv'
    'M15_PWR_n3_L16_v1_line.csv'
    'M16_PWR_n5_L16_v1_line.csv'
};

% Labels to display in plots
modelLabels = {
    'n = 1.5'
    'n = 2'
    'n = 3'
    'n = 5'
};

% Output folder for figures
outFolder = fullfile(dataFolder, 'phaseB_figures');
if ~exist(outFolder, 'dir')
    mkdir(outFolder);
end

%% === READ SUMMARY ===

summaryTbl = readtable(summaryFile);

disp('=== SUMMARY TABLE ===');
disp(summaryTbl);

%% === SORT SUMMARY IN DESIRED ORDER ===

desiredOrder = {
    'M13_PWR_n1p5_L16_v1'
    'M14_PWR_n2_L16_v1'
    'M15_PWR_n3_L16_v1'
    'M16_PWR_n5_L16_v1'
};

[~, idxOrder] = ismember(desiredOrder, summaryTbl.model_name);
summaryTbl = summaryTbl(idxOrder, :);

%% === PLOT 1: S11(x) profiles ===

figure('Color', 'w');
hold on; grid on; box on;

lineTables = cell(numel(lineFiles),1);

for i = 1:numel(lineFiles)
    T = readtable(fullfile(dataFolder, lineFiles{i}));
    
    % If there are two rows for each x position, average values by x
    [xUnique, ~, ic] = unique(T.x);
    s11Mean = accumarray(ic, T.S11, [], @mean);
    misesMean = accumarray(ic, T.Mises, [], @mean);
    
    Tmean = table(xUnique, s11Mean, misesMean, ...
        'VariableNames', {'x','S11','Mises'});
    
    lineTables{i} = Tmean;
    
    plot(Tmean.x, Tmean.S11, 'LineWidth', 2, 'DisplayName', modelLabels{i});
end

xlabel('x [mm]');
ylabel('S11 [MPa]');
title('Phase B - Comparison of S11(x) profiles');
legend('Location', 'best');
set(gca, 'FontSize', 11);

saveas(gcf, fullfile(outFolder, 'phaseB_S11_profiles.png'));

%% === PLOT 2: von Mises(x) profiles ===

figure('Color', 'w');
hold on; grid on; box on;

for i = 1:numel(lineTables)
    Tmean = lineTables{i};
    plot(Tmean.x, Tmean.Mises, 'LineWidth', 2, 'DisplayName', modelLabels{i});
end

xlabel('x [mm]');
ylabel('von Mises [MPa]');
title('Phase B - Comparison of von Mises(x) profiles');
legend('Location', 'best');
set(gca, 'FontSize', 11);

saveas(gcf, fullfile(outFolder, 'phaseB_Mises_profiles.png'));

%% === PLOT 3: Global peaks comparison ===

figure('Color', 'w');

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

saveas(gcf, fullfile(outFolder, 'phaseB_global_peaks.png'));

%% === PLOT 4: Peak position shift ===

figure('Color', 'w');
hold on; grid on; box on;

plot(1:height(summaryTbl), summaryTbl.max_mises_x, '-o', 'LineWidth', 2, 'MarkerSize', 7);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 11);

xlabel('Model');
ylabel('x position of max von Mises [mm]');
title('Shift of von Mises peak position');

saveas(gcf, fullfile(outFolder, 'phaseB_peak_position.png'));

%% === FINAL TABLE FOR DECISION ===

finalTbl = table;
finalTbl.Model = modelLabels;
finalTbl.MaxMises = summaryTbl.max_mises;
finalTbl.MaxMises_X = summaryTbl.max_mises_x;
finalTbl.MaxS11 = summaryTbl.max_s11;
finalTbl.MaxS11_X = summaryTbl.max_s11_x;
finalTbl.MinS11 = summaryTbl.min_s11;
finalTbl.MinS11_X = summaryTbl.min_s11_x;

writetable(finalTbl, fullfile(outFolder, 'phaseB_final_table.csv'));

disp('=== FINAL DECISION TABLE ===');
disp(finalTbl);

%% === SIMPLE AUTOMATIC INDICATION ===

[~, idxBestMises] = min(summaryTbl.max_mises);
[~, idxBestMinS11] = max(summaryTbl.min_s11);  
% max() is used because the values are negative: -6.8 is better than -8.1

fprintf('\n');
fprintf('Best model for max von Mises: %s\n', modelLabels{idxBestMises});
fprintf('Best model for min S11: %s\n', modelLabels{idxBestMinS11});

if idxBestMises == idxBestMinS11
    fprintf('Strong automatic candidate: %s\n', modelLabels{idxBestMises});
else
    fprintf('Final evaluation of S11(x) profiles is still required.\n');
end

fprintf('\nFigures saved in:\n%s\n', outFolder);
