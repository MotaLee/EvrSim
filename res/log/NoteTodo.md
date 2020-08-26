# Update Log

---

## Most recent

version: [0.0.6](#details)

Date:2020/00/00

---

## Note

'todo' in files
map/model: save as
help: manual/about/read me
edit: undo/redo
function to achieve: command panel/setting dialog
data record
aroglc: scale ruler/toolbar optimize
dynamics: constraint solution/__rigid dynamics__
arocore: visualization
detail tab: __pick aro__
next goal: planar machine

---

## Details

0.0.6 - 2020/00/00:

1. Mods:
    * AroCore: Added tracks of the point display as a tool;
    * AroCore: Added a keyword 'AROCLASS_ABBR' to 'AcpSelector'/'AcpProvider';
    * AroCore: Added Adp 'AdpArrow'/'AdpImage';
    * AroCore: Added Aro 'AroImage';
    * AroCore: Added Acp 'AcpLimitor';
    * AroCore: Added tool 'ALibs' to show all supported Aro/Acp;
    * Dynamics: Added Aro 'PointForce';
    * AroPlot: Added 'FigurePlc' control;
    * STS: Added lots of tools;
2. Fixed the unexpected event distribution of tools in the Aro/Mod panel;
3. App:
    * Renamed 'EvrSimWx.py' to 'EvrSimEditor.py'
    * Added 'app' folder, and EvrSimEditor/EST moved into it;
    * Added new application 'SmartToeSleeve' and its sim 'sts';
4. Added 'res' folder, and many resources folder moved into it;
5. Side panel：
    * Added 'Workspace toggle', 'Detail' and 'Manager' button；
    * Removed Other tab button, while their functions moved to 'Manager'/'Detail' tab;
6. Core module 'esui':
    * Added Tree relavant controls;
    * Added the 'MapDialog' control;
    * Added the 'HintText' control;
    * Optimized the 'Mtc' control;
    * Renamed text relavant controls to meaningful names;
    * Added 'window' control intergrated from the legacy of 'EvrSimWx';
    * Optimized global variables, and now an app needn't to deal the client display;
7. Core module 'esc':
    * Fixed a bug while running sim with no model enabled;
    * Added 'renameMapFile' method;
    * Added 'ES_PATH' global variable;
    * Adjusted the algorithm of running sim for supporting static calculation;
8. Head panel:
    * Achieved the function of renaming the map;
    * Achieved the function of renaming the model;
9. Acp panel:
    * Optimized the connections of Acps;
    * Added displaying the head of model;
    * Optimized the operation of adding Acp;
    * Decreased the frequency of flicking;
    * Optimized the behavior of attaching Acps;
    * Added __Copy/Cut/Paste__ Acp functions which can also be called in Head panel;
10. Command panel:
    * Rebinded the method 'ESC.bug', and now using this method will display the bug information in Command panel;
    * Unbind the relation of other panels, and now use event to open/close;
    * Renamed 'COM_PLC' to 'CMD_PLC' in esui;
11. Core module 'esevt':
    * Added new events 'EVT_OPEN_CMD' and 'EVT_CLOSE_CMD';
    * Optimized variable names;
12. Core module 'esgl':
    * Added 'genTexture' method, now supporting base texture display;
    * Added lots of openGL methods, and optimized the performance;
13. Core module 'estool':
    * Moved Mod panel(plc_Mod) form esui and renamed to Tool panel(tool_plc);
    * Massively optimized tool relavant structure, including modified all mods;

---
