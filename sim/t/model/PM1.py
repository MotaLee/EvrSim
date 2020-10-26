ACP_INDEX=[1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26]
KEY_DICT={1: 'AcpID', 2: 'AcpClass', 3: 'position', 4: 'fixIO', 5: 'port', 6: 'inport', 7: 'outport', 8: 'AcpName', 9: 'desc', 10: 'static', 11: 'script', 12: 'expression', 13: 'item', 14: 'default'}
Acp_1={1: 1, 2: 'mod.Dynamics.acp.IPE', 3: [691, 518], 4: 'Neither', 5: {}, 6: {}, 7: {}, 8: 'IPE', 9: '', 10: False, 11: ''}
Acp_11={1: 11, 2: 'mod.AroCore.acp.AcpProvider', 3: [691, 172], 4: 'Both', 5: {1: 'in'}, 6: {1: (12, 2)}, 7: {}, 8: 'f_RG', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='RigidGroup'", 13: 'force'}
Acp_12={1: 12, 2: 'mod.AroCore.acp.AcpSum', 3: [864, 172], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (13, 1)}, 7: {2: [(11, 1)]}, 8: 'New Acp', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='RigidGroup'", 13: 'force'}
Acp_13={1: 13, 2: 'mod.AroCore.acp.AcpSelector', 3: [1036, 172], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(12, 1)]}, 8: 'f_MP', 9: '', 10: False, 11: '', 12: "AROVE['AroID'] in SELF_ARO.children", 13: 'force', 14: 0}
Acp_14={1: 14, 2: 'mod.AroCore.acp.AcpProvider', 3: [172, 172], 4: 'Both', 5: {1: 'in'}, 6: {1: (16, 2)}, 7: {}, 8: 'f_MP', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='MassPoint'", 13: 'force', 14: 0}
Acp_15={1: 15, 2: 'mod.AroCore.acp.AcpSelector', 3: [518, 172], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(16, 1)]}, 8: 'fSlctr', 9: '', 10: False, 11: '', 12: "SELF_ARO.AroID in ARO.targets and ARO.tag=='force'", 13: 'value', 14: [0, 0, 0]}
Acp_16={1: 16, 2: 'mod.AroCore.acp.AcpSum', 3: [343, 172], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (15, 1)}, 7: {2: [(14, 1)]}, 8: 'New Acp', 9: '', 10: False, 11: '', 12: "SELF_ARO.AroID in ARO.targets and ARO.tag=='force'", 13: 'value', 14: [0, 0, 0]}
Acp_17={1: 17, 2: 'mod.AroCore.acp.AcpProvider', 3: [172, 345], 4: 'Both', 5: {1: 'in'}, 6: {1: (18, 2)}, 7: {}, 8: 'T_RG', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='RigidGroup'", 13: 'moment', 14: [0, 0, 0]}
Acp_18={1: 18, 2: 'mod.AroCore.acp.AcpSum', 3: [345, 345], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (19, 0)}, 7: {2: [(17, 1)]}, 8: 'Acp', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='RigidGroup'", 13: 'moment', 14: [0, 0, 0]}
Acp_19={1: 19, 2: 'mod.AroCore.acp.AcpCross', 3: [518, 345], 4: 'Both', 5: {0: 'out r', 1: 'in a', 2: 'in b'}, 6: {1: (20, 0), 2: (22, 1)}, 7: {0: [(18, 1)]}, 8: 'Acpz6', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='RigidGroup'", 13: 'moment', 14: [0, 0, 0]}
Acp_20={1: 20, 2: 'mod.AroCore.acp.AcpPMTD', 3: [777, 345], 4: 'Out', 5: {0: 'out R', 1: 'in a', 2: 'in b'}, 6: {1: (23, 1), 2: (24, 1)}, 7: {0: [(19, 1)]}, 8: 'Acpz7', 9: '', 10: False, 11: '', 12: 'b-a', 13: 'moment', 14: [0, 0, 0]}
Acp_22={1: 22, 2: 'mod.AroCore.acp.AcpSelector', 3: [691, 432], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(19, 2)]}, 8: 'Acp', 9: '', 10: False, 11: '', 12: 'ARO.AroID in SELF_ARO.children', 13: 'force', 14: [0, 0, 0]}
Acp_23={1: 23, 2: 'mod.AroCore.acp.AcpSelector', 3: [950, 345], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(20, 1)]}, 8: 'mcp_RG', 9: '', 10: False, 11: '', 12: 'ARO.AroID==SELF_ARO.AroID', 13: 'position', 14: [0, 0, 0]}
Acp_24={1: 24, 2: 'mod.AroCore.acp.AcpSelector', 3: [950, 432], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(20, 2)]}, 8: 'pSlctr', 9: '', 10: False, 11: '', 12: 'ARO.AroID in SELF_ARO.children', 13: 'position', 14: 0}
Acp_25={1: 25, 2: 'mod.AroCore.acp.AcpProvider', 3: [172, 518], 4: 'Both', 5: {1: 'in'}, 6: {1: (26, 1)}, 7: {}, 8: 'P_CON', 9: '', 10: False, 11: '', 12: "ABBRCLASS=='Constraint'", 13: 'position', 14: 0}
Acp_26={1: 26, 2: 'mod.AroCore.acp.AcpSelector', 3: [345, 518], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(25, 1)]}, 8: 'Acp_26', 9: '', 10: False, 11: '', 12: 'ARO.AroID==SELF_ARO.m_target', 13: 'position', 14: [0, 0, 0]}
