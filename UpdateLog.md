# Update

---

## Note

'todo' in files
map: save as/rename/delete
model: save as/rename/delete
sim: manager
help: manual/about/read me
edit: undo/redo/copy/cut/paste
function to achieve: command panel/setting dialog
acp limitor
data record
aroglc: scale ruler/toolbar optimize
dynamics: point force/constraint solution/track/visualize
0.0.5 goal: planar machine

---

## Log

0.0.5 - 2020/07/19:

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

0.0.4 - 2020/06/27:

1. Universal gravity model finished;
2. Lots of Acp bugs fixed;

0.0.3 - 2020/06/22:

1. Base frame finished;

0.0.2 - 2020/05/18:

1. UpdateLog created;

0.0.1 - 2020/04/01:

1. First initilization;

---
