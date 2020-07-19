ACP_INDEX=[1, 2, 3, 4, 5, 6, 14]
KEY_DICT={1: 'AcpID', 2: 'AcpClass', 3: 'position', 4: 'fixIO', 5: 'inport', 6: 'outport', 7: 'AcpName', 8: 'desc', 9: 'port', 10: 'expression', 11: 'item', 12: 'current', 13: 'start', 14: 'step', 15: 'end'}
Acp_1={1: 1, 2: 'mod.AroCore.acp.AcpProvider', 3: [114, 95], 4: 'Both', 5: {1: (2, 0)}, 6: {}, 7: 'm2', 8: '', 9: {1: 'in'}, 10: "ARO.AroName=='m2'", 11: 'position'}
Acp_2={1: 2, 2: 'mod.AroCore.acp.AcpPMTD', 3: [261, 88], 4: 'Out', 5: {1: (4, 1), 2: (5, 1), 3: (3, 1)}, 6: {0: [(1, 1)]}, 7: 'New Acp', 8: '', 9: {0: 'out r', 1: 'in a', 2: 'in b', 3: 'in c'}, 10: 'a+b*c'}
Acp_3={1: 3, 2: 'mod.AroCore.acp.AcpIterator', 3: [586, 371], 4: 'Both', 5: {}, 6: {1: [(2, 3), (14, 3)], 2: []}, 7: 'New Acp', 8: '', 9: {1: 'step out', 2: 'current out'}, 11: 'time', 12: 17.50000000000003, 13: 0, 14: 0.1, 15: 1}
Acp_4={1: 4, 2: 'mod.AroCore.acp.AcpSelector', 3: [591, 234], 4: 'Both', 5: {}, 6: {1: [(2, 1), (14, 2)]}, 7: 'p_m2', 8: '', 9: {1: 'out'}, 10: 'ARO==SELF_ARO', 11: 'position'}
Acp_5={1: 5, 2: 'mod.AroCore.acp.AcpSelector', 3: [579, 77], 4: 'Both', 5: {}, 6: {1: [(2, 2), (14, 1)]}, 7: 'v_m2', 8: '', 9: {1: 'out'}, 10: 'ARO==SELF_ARO', 11: 'velocity'}
Acp_6={1: 6, 2: 'mod.AroCore.acp.AcpProvider', 3: [106, 269], 4: 'Both', 5: {1: (14, 0)}, 6: {}, 7: 'prdr_m2_v', 8: '', 9: {1: 'in'}, 10: "ARO.AroName=='m2'", 11: 'velocity'}
Acp_14={1: 14, 2: 'mod.AroCore.acp.AcpPMTD', 3: [254, 256], 4: 'Out', 5: {1: (5, 1), 2: (4, 1), 3: (3, 1)}, 6: {0: [(6, 1)]}, 7: 'New Acp', 8: '', 9: {0: 'out r', 1: 'in a', 2: 'in b', 3: 'in c'}, 10: 'a-b*c'}
