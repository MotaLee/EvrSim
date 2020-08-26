ACP_INDEX=[1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
KEY_DICT={1: 'AcpID', 2: 'AcpClass', 3: 'position', 4: 'fixIO', 5: 'port', 6: 'inport', 7: 'outport', 8: 'AcpName', 9: 'desc', 10: 'expression', 11: 'item', 12: 'default', 13: 'current', 14: 'start', 15: 'step', 16: 'end', 17: 'up', 18: 'low', 19: 'up_trigger', 20: 'low_trigger'}
Acp_1={1: 1, 2: 'mod.AroCore.acp.AcpProvider', 3: [84, 91], 4: 'Both', 5: {1: 'in'}, 6: {1: (2, 0)}, 7: {}, 8: 'New Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'v'}
Acp_2={1: 2, 2: 'mod.AroCore.acp.AcpPMTD', 3: [468, 106], 4: 'Out', 5: {0: 'out r', 1: 'in a', 2: 'in b'}, 6: {1: (3, 1), 2: (5, 0)}, 7: {0: [(1, 1), (13, 1)]}, 8: 'New Acp', 9: '', 10: 'a+b', 11: 'v'}
Acp_3={1: 3, 2: 'mod.AroCore.acp.AcpSelector', 3: [715, 98], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(2, 1)]}, 8: 'New Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'v', 12: 0}
Acp_5={1: 5, 2: 'mod.AroCore.acp.AcpPMTD', 3: [595, 257], 4: 'Out', 5: {0: 'out r', 1: 'in a', 2: 'in b', 3: 'in P', 4: 'in P'}, 6: {1: (9, 1), 2: (10, 1), 3: (7, 1), 4: (6, 1)}, 7: {0: [(2, 2)]}, 8: 'New Acp', 9: '', 10: '(a-b)*d/c', 11: 'v', 12: 0}
Acp_6={1: 6, 2: 'mod.AroCore.acp.AcpIterator', 3: [970, 341], 4: 'Both', 5: {1: 'step out', 2: 'current out'}, 6: {}, 7: {1: [(13, 2), (5, 4)], 2: []}, 8: 'New Acp', 9: '', 10: '(a-b)*d/c', 11: 'time', 12: 0, 13:0, 14: 0, 15: 0.01, 16: 1}
Acp_7={1: 7, 2: 'mod.AroCore.acp.AcpSelector', 3: [992, 210], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(5, 3)]}, 8: 'New Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'mass', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_9={1: 9, 2: 'mod.AroCore.acp.AcpSelector', 3: [854, 85], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(5, 1)]}, 8: 'New Acp', 9: '', 10: "ARO.AroName=='pipe'", 11: 'cur_pressure', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_10={1: 10, 2: 'mod.AroCore.acp.AcpSelector', 3: [981, 90], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(5, 2)]}, 8: 'New Acp', 9: '', 10: "ARO.AroName=='pistol'", 11: 'cur_pressure', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_11={1: 11, 2: 'mod.AroCore.acp.AcpProvider', 3: [15, 342], 4: 'Both', 5: {1: 'in'}, 6: {1: (12, 4)}, 7: {}, 8: 'Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'position', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_12={1: 12, 2: 'mod.AroCore.acp.AcpVector3', 3: [149, 339], 4: 'Both', 5: {1: 'in x', 2: 'in y', 3: 'in z', 4: 'out vec3'}, 6: {1: (16, 2), 2: (14, 3), 3: (14, 4)}, 7: {4: [(11, 1)]}, 8: 'Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'position', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_13={1: 13, 2: 'mod.AroCore.acp.AcpPMTD', 3: [386, 350], 4: 'Out', 5: {0: 'out r', 1: 'in a', 2: 'in b', 3: 'in P'}, 6: {1: (2, 0), 2: (6, 1), 3: (14, 2)}, 7: {0: [(16, 1)]}, 8: 'Acp', 9: '', 10: 'c+a*b', 11: 'position', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_14={1: 14, 2: 'mod.AroCore.acp.AcpDepartor3', 3: [557, 611], 4: 'Both', 5: {1: 'in vec3', 2: 'out x', 3: 'out y', 4: 'out z'}, 6: {1: (15, 1)}, 7: {2: [(13, 3)], 3: [(12, 2)], 4: [(12, 3)]}, 8: 'Acp', 9: '', 10: 'c+a*b', 11: 'position', 12: 0, 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_15={1: 15, 2: 'mod.AroCore.acp.AcpSelector', 3: [768, 497], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(14, 1)]}, 8: 'Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'position', 12: [0, 0, 0], 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1}
Acp_16={1: 16, 2: 'mod.AroCore.acp.AcpLimitor', 3: [263, 252], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (13, 0)}, 7: {2: [(12, 1)]}, 8: 'Acp', 9: '', 10: "ARO.AroName=='toe_sleeve'", 11: 'position', 12: [0, 0, 0], 13: 1.8000000000000023, 14: 0, 15: 0.01, 16: 1, 17: 0, 18: 'Inf', 19: None, 20: None}
