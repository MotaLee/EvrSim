ACP_INDEX=[1, 2, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
KEY_DICT={1: 'AcpID', 2: 'AcpClass', 3: 'position', 4: 'fixIO', 5: 'inport', 6: 'outport', 7: 'AcpName', 8: 'desc', 9: 'port', 10: 'expression', 11: 'item', 12: 'value', 13: 'current', 14: 'start', 15: 'step', 16: 'end'}
Acp_1={1: 1, 2: 'mod.AroCore.acp.AcpSelector', 3: [1361.0, 633.0], 4: 'Both', 5: {}, 6: {1: [(6, 2), (21, 1)]}, 7: 'pSelf', 8: '', 9: {1: 'out'}, 10: 'SELF_AROID==ARO.AroID', 11: 'position'}
Acp_2={1: 2, 2: 'mod.AroCore.acp.AcpProvider', 3: [39.0, 257.0], 4: 'Both', 5: {1: (8, 0)}, 6: {}, 7: 'fPvdr', 8: '', 9: {1: 'in'}, 10: '"force" in AROVE', 11: 'force'}
Acp_5={1: 5, 2: 'mod.AroCore.acp.AcpSelector', 3: [1319.0, 416.0], 4: 'Both', 5: {}, 6: {1: [(6, 1)]}, 7: 'pOther', 8: '', 9: {1: 'out'}, 10: 'SELF_AROID!=ARO.AroID and "position" in AROVE', 11: 'position'}
Acp_6={1: 6, 2: 'mod.AroCore.acp.AcpPMTD', 3: [1097.0, 479.0], 4: 'Out', 5: {1: (5, 1), 2: (1, 1)}, 6: {3: [(13, 1), (14, 2)]}, 7: 'rij', 8: '', 9: {1: 'in a', 2: 'in b', 3: 'out r'}, 10: 'a-b'}
Acp_7={1: 7, 2: 'mod.AroCore.acp.AcpSum', 3: [444, 536], 4: 'Both', 5: {1: (14, 0)}, 6: {2: [(8, 3)]}, 7: 'mr/r3', 8: '', 9: {1: 'in', 2: 'out'}}
Acp_8={1: 8, 2: 'mod.AroCore.acp.AcpPMTD', 3: [317.0, 236.0], 4: 'Out', 5: {1: (9, 1), 2: (12, 1), 3: (7, 2)}, 6: {0: [(2, 1), (18, 2)]}, 7: 'fout', 8: '', 9: {1: 'in a', 2: 'in b', 0: 'out r', 3: 'in c'}, 10: 'a*b*c'}
Acp_9={1: 9, 2: 'mod.AroCore.acp.AcpConst', 3: [818, 379], 4: 'Both', 5: {}, 6: {1: [(8, 1)]}, 7: 'constG', 8: '', 9: {1: 'out'}, 11: 'G', 12: 0.1}
Acp_12={1: 12, 2: 'mod.AroCore.acp.AcpSelector', 3: [820, 263], 4: 'Both', 5: {}, 6: {1: [(8, 2), (18, 4)]}, 7: 'mSelf', 8: '', 9: {1: 'out'}, 10: 'SELF_AROID==ARO.AroID and "mass" in AROVE', 11: 'mass'}
Acp_13={1: 13, 2: 'mod.AroCore.acp.AcpNorm', 3: [873.0, 558.0], 4: 'Both', 5: {1: (6, 3)}, 6: {2: [(14, 3)]}, 7: 'rijNorm', 8: '', 9: {1: 'in vec', 2: 'out norm'}}
Acp_14={1: 14, 2: 'mod.AroCore.acp.AcpPMTD', 3: [652, 535], 4: 'Out', 5: {1: (15, 1), 2: (6, 3), 3: (13, 2)}, 6: {0: [(7, 1)]}, 7: 'New Acp', 8: '', 9: {1: 'in a', 2: 'in b', 0: 'out r', 3: 'in c'}, 10: 'a/c**3*b'}
Acp_15={1: 15, 2: 'mod.AroCore.acp.AcpSelector', 3: [1096, 359], 4: 'Both', 5: {}, 6: {1: [(14, 1)]}, 7: 'mOther', 8: '', 9: {1: 'out'}, 10: 'SELF_AROID!=ARO.AroID and "mass" in AROVE', 11: 'mass'}
Acp_16={1: 16, 2: 'mod.AroCore.acp.AcpProvider', 3: [4.0, 143.0], 4: 'Both', 5: {1: (18, 0)}, 6: {}, 7: 'vPvdr', 8: '', 9: {1: 'in'}, 10: '"velocity" in AROVE', 11: 'velocity'}
Acp_17={1: 17, 2: 'mod.AroCore.acp.AcpIterator', 3: [810, 126], 4: 'Both', 5: {}, 6: {1: [(18, 3), (21, 2)], 2: []}, 7: 'tItor', 8: '', 9: {1: 'step out', 2: 'current out'}, 11: 'time', 13: 310.466666666698, 14: 0, 15: 0.1, 16: 0}
Acp_18={1: 18, 2: 'mod.AroCore.acp.AcpPMTD', 3: [302.0, 27.0], 4: 'Out', 5: {1: (19, 1), 2: (8, 0), 3: (17, 1), 4: (12, 1)}, 6: {0: [(16, 1), (21, 3)]}, 7: 'vout', 8: '', 9: {0: 'out r', 1: 'in a', 2: 'in b', 3: 'in c', 4: 'in d'}, 10: 'a+b*c/d'}
Acp_19={1: 19, 2: 'mod.AroCore.acp.AcpSelector', 3: [809, 16], 4: 'Both', 5: {}, 6: {1: [(18, 1)]}, 7: 'New Acp', 8: '', 9: {1: 'out'}, 10: '"velocity" in AROVE and SELF_AROID==ARO.AroID', 11: 'velocity'}
Acp_20={1: 20, 2: 'mod.AroCore.acp.AcpProvider', 3: [3.0, 648.0], 4: 'Both', 5: {1: (21, 0)}, 6: {}, 7: 'pPvdr', 8: '', 9: {1: 'in'}, 10: True, 11: 'position'}
Acp_21={1: 21, 2: 'mod.AroCore.acp.AcpPMTD', 3: [227.0, 647.0], 4: 'Out', 5: {1: (1, 1), 2: (17, 1), 3: (18, 0)}, 6: {0: [(20, 1)]}, 7: 'pout', 8: '', 9: {0: 'out r', 1: 'in a', 2: 'in b', 3: 'in c'}, 10: 'a+b*c'}
