# Note

'todo' in files
map/model: save as
help: manual/about/read me
edit: undo/redo
function to achieve: command panel/setting dialog
aroglc: scale ruler/toolbar optimize/__better selecting__
acpplc: comment acp
aroplot: visualization
detail tab: quick view/arospace folder
esc: data record
next goal: multi-thread acp/compiled models running

---

## Next Update

### 0.0.8 - 2020/10/00

1. App:
2. Mod:
    * Moved some tools from AroCore to AroPlot;
    * Added a real-time clock text tool in AroCore;
3. esui:
    * Cancelled the multi-threading of EsWindow;
    * Added mod manager to load new mod in Headbar;
4. esmdl:
    * Fixed the bug that acps would be selected when dismissing the detail dialog;
5. esc:
    * Added a global variable 'ARO_ORDER';
    * Delete a global variable 'AROID_MAX', and its function was replaced by 'ARO_ORDER';
    * Added new methods 'sortAro' and 'sortAroMap';
    * Added new methods 'runCompiledSim' and 'compileModel' to boost performance, not fully completed yet but working;
6. esgl:
    * Optimized the performance of 'drawGL' method;
    * Moved toolbar to AroCore;
7. estab:
    * Fixed some bugs with MapTreePlc;
    * Added the icon to items of the tree plc;
    * Achieved dragging sorting of MapTreePlc;
    * Added relavant controls of picking Aroes in detail tab;

---
