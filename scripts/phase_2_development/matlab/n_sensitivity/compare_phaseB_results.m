clear; clc; close all;

%% =========================================================
%  PHASE B - POWER LAW SENSITIVITY COMPARISON
%  Legge:
%  n = 1.5, 2, 3, 5
%  Input atteso nella cartella corrente oppure specificata
%% =========================================================

%% === USER SETTINGS ===

% Cartella dove stanno i CSV
dataFolder = pwd;

% File summary
summaryFile = fullfile(dataFolder, 'summary_phaseB.csv');

% File line profiles
lineFiles = {
    'M13_PWR_n1p5_L16_v1_line.csv'
    'M14_PWR_n2_L16_v1_line.csv'
    'M15_PWR_n3_L16_v1_line.csv'
    'M16_PWR_n5_L16_v1_line.csv'
};

% Etichette da mostrare nei grafici
modelLabels = {
    'n = 1.5'
    'n = 2'
    'n = 3'
    'n = 5'
};

% Cartella output figure
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
    
    % Se ci sono due righe per ogni x (y=2.85 e y=3.15), facciamo media per x
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
title('Phase B - Confronto profili S11(x)');
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
title('Phase B - Confronto profili von Mises(x)');
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
title('Spostamento della posizione del picco di von Mises');

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
% max() perché i valori sono negativi: -6.8 è "meglio" di -8.1

fprintf('\n');
fprintf('Miglior modello per max von Mises: %s\n', modelLabels{idxBestMises});
fprintf('Miglior modello per min S11: %s\n', modelLabels{idxBestMinS11});

if idxBestMises == idxBestMinS11
    fprintf('Candidato automatico forte: %s\n', modelLabels{idxBestMises});
else
    fprintf('Serve valutazione finale sui profili S11(x).\n');
end

fprintf('\nFigure salvate in:\n%s\n', outFolder);