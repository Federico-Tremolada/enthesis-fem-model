clear; clc; close all;

%% =========================================================
%  PHASE C - POISSON COMPARISON
%  Confronto:
%  M17 = nu costante
%  M18 = nu variabile
%% =========================================================

%% === USER SETTINGS ===
dataFolder = pwd;

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

    % Se per ogni x hai due y vicine alla mezzeria, faccio media per x
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
title('Fase C - Confronto profili S11(x)');
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
title('Fase C - Confronto profili von Mises(x)');
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
ylabel('x posizione picco von Mises [mm]');
title('Posizione x picco von Mises');
grid on; box on;

nexttile;
plot(1:height(summaryTbl), summaryTbl.max_mises_y, '-o', 'LineWidth', 2, 'MarkerSize', 7);
set(gca, 'XTick', 1:height(summaryTbl), 'XTickLabel', modelLabels, 'FontSize', 11);
ylabel('y posizione picco von Mises [mm]');
title('Posizione y picco von Mises');
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
fprintf('Variazione max von Mises (nu variabile vs costante): %+0.2f %%\n', deltaMises);
fprintf('Variazione |min S11| (nu variabile vs costante): %+0.2f %%\n', deltaMinS11);
fprintf('\nFigure salvate in:\n%s\n', outFolder);