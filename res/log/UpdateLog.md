# Update Log

---

## Most recent

version: [0.0.6](#details)

Date:2020/08/26

---

## Details

### 0.0.7 - 2020/09/00

1. App:
    * SmartToeSleeve: Optimized some details;
    * Editor: Added a splash;
2. Mod:
    * AroPlot: Optimized variables and the redrawing method;
    * AroCore: Added a new acp 'AcpExecutor';
    * Dynamics: Added a new acp 'IPE' form AcpExecutor and achieved simple constrainted planar machines;
3. esui:
    * Added an icon of EvrSim to EsWindow control;
    * Added a global class 'ESFont' to simplify calling a font;
4. esmdl:
    * Added a new core module from 'plc_Acp';
    * Fixed lots of operating bugs;
5. esc:
    * Massively optimized running performance;
    * Added lots of performance relavant variables;

### 0.0.6 - 2020/08/26

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

### 0.0.5 - 2020/07/19

1. Manual document added;
2. language pack added; [1]
3. Core module 'esui':
    * Global variable optimized;
    * UI 'MenuBtn'/'SelectMenuBtn' neednt rebind events after calling method 'setItems';
    * Added scrollable container "ScrolledPlc";
4. Core module 'esgl'/Aro Panel:
    * Global variable optimized;
    * Added response to 'EVT_LOAD_MOD';
    * All HUDs moved to mod AroCore as tools;
    * Toolbar added;
    * Toobar added 'Select'/'Rect Select' button, achieved 'Del' button;
    * Rectangle selecting and multi-selecting achieved;
    * Drawpart attribute 'fix_size' achieved;
    * Drawpart attribute 'fix_oritation' achieved;
    * Method 'importDPM' added, and use it to import the 3D model for drawpart;
5. Head panel:
    * Command panel added, and click 'ES' in head panel to show it;
    * Minimizing button added;
    * Sim menu: 'Save as'/'Setting'/'Close' item achieved;
    * Map menu: 'New' item achieved;
6. Acp panel:
    * Rectangle selecting and multi-selecting added;
    * Toolbar added;
    * Acp node remove/move button removed;
    * Remove/move/attach to grid button added;
7. Side panel:
    * Acp detail panel added ports display;
    * added response to the common event;
    * Aro list view changed to tree view;
    * Adding inport of Acp achieved;
8. Mods:
    * AroCore: 'Aro' Aro class added 'onSet'/'onDel' metohod and ESC optimized;
    * AroCore: Aro class 'AroTree'/'AroGroup'/'AroTarget' added;
    * AroCore: Tool 'New Aro' removed;
    * AroCore: Attribute 'fixIO' of 'Acp' changed to enum variable with Both/In/Out/Neither status instead of bool;
    * AroCore: Viewball HUD added;
    * AroCore: Tool 'Rst' multi-refreshing bug fixed;
    * AroPlot: new module 'AroPlot' added;
    * Dynamics: Aro class 'RigidGroup' and its relavant tools added;
    * Dynamics: Aro class 'Moment' and its drawpart added;
9. Core module 'esc':
    * ESC packaged instead of a single file;
    * Varialbe USER_SETTING unstable bug fixed, and now loading mods'setting before the sim's when opening the sim;
10. Core module 'esevt':
    * Event 'EVT_COMMON_EVENT'/'EVT_UPDATE_MAP'/'EVT_UPDATE_MODEL' added;
    * Common event dealing achieved by sending it and special event type as args, then all panels would respond it;
11. Libs:
    * PyGLM: upgraded to 1.99.1, and fixed bugs with numpy;
12. Update logs moved form 'README.md' to 'UpdateLog.md';

---

### 0.0.4 - 2020/06/27

1. Universal gravity model finished;
2. Lots of Acp bugs fixed;

---

### 0.0.3 - 2020/06/22

1. Base frame finished;

---

### 0.0.2 - 2020/05/18

1. UpdateLog created;

---

### 0.0.1 - 2020/04/01

1. First initilization;

---
