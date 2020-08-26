ACP_INDEX=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
KEY_DICT={1: 'AcpID', 2: 'AcpClass', 3: 'position', 4: 'fixIO', 5: 'port', 6: 'inport', 7: 'outport', 8: 'AcpName', 9: 'desc', 10: 'expression', 11: 'item', 12: 'default'}
Acp_1={1: 1, 2: 'mod.AroCore.acp.AcpProvider', 3: [170, 86], 4: 'Both', 5: {1: 'in'}, 6: {1: (2, 2)}, 7: {}, 8: 'New Acp', 9: '', 10: "AROCLASS_ABBR=='RigidGroup'", 11: 'mass'}
Acp_2={1: 2, 2: 'mod.AroCore.acp.AcpSum', 3: [498, 88], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (3, 1)}, 7: {2: [(1, 1), (5, 1)]}, 8: 'New Acp', 9: '', 10: "AROCLASS_ABBR=='RigidGroup'", 11: 'mass'}
Acp_3={1: 3, 2: 'mod.AroCore.acp.AcpSelector', 3: [827, 84], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(2, 1), (8, 1)]}, 8: 'mSlctr', 9: '', 10: "AROVE['AroID'] in SELF_ARO.children", 11: 'mass', 12: 0}
Acp_4={1: 4, 2: 'mod.AroCore.acp.AcpProvider', 3: [166, 252], 4: 'Both', 5: {1: 'in'}, 6: {1: (5, 0)}, 7: {}, 8: 'p_RG', 9: '', 10: "AROCLASS_ABBR=='RigidGroup'", 11: 'position', 12: 0}
Acp_5={1: 5, 2: 'mod.AroCore.acp.AcpPMTD', 3: [332, 249], 4: 'Out', 5: {0: 'out r', 1: 'in a', 2: 'in b'}, 6: {1: (2, 2), 2: (6, 2)}, 7: {0: [(4, 1)]}, 8: 'Smr/Sm', 9: '', 10: 'b/a', 11: 'position', 12: 0}
Acp_6={1: 6, 2: 'mod.AroCore.acp.AcpSum', 3: [497, 249], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (8, 0)}, 7: {2: [(5, 2)]}, 8: 'New Acp', 9: '', 10: 'b/a', 11: 'position', 12: 0}
Acp_7={1: 7, 2: 'mod.AroCore.acp.AcpSelector', 3: [829, 251], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(8, 2)]}, 8: 'pSlctr', 9: '', 10: "AROVE['AroID'] in SELF_ARO.children", 11: 'position', 12: 0}
Acp_8={1: 8, 2: 'mod.AroCore.acp.AcpPMTD', 3: [663, 249], 4: 'Out', 5: {0: 'out r', 1: 'in a', 2: 'in b'}, 6: {1: (3, 1), 2: (7, 1)}, 7: {0: [(6, 1)]}, 8: 'mr', 9: '', 10: 'a*b', 11: 'position', 12: 0}
Acp_9={1: 9, 2: 'mod.AroCore.acp.AcpProvider', 3: [662, 417], 4: 'Both', 5: {1: 'in'}, 6: {1: (10, 1)}, 7: {}, 8: 'p_PF', 9: '', 10: "AROCLASS_ABBR=='PointForce'", 11: 'position', 12: 0}
Acp_10={1: 10, 2: 'mod.AroCore.acp.AcpSelector', 3: [828, 414], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(9, 1)]}, 8: 'New Acp', 9: '', 10: "AROVE['AroID'] in SELF_ARO.targets", 11: 'position', 12: 0}
Acp_11={1: 11, 2: 'mod.AroCore.acp.AcpProvider', 3: [168, 417], 4: 'Both', 5: {1: 'in'}, 6: {1: (12, 2)}, 7: {}, 8: 'f_RG', 9: '', 10: "AROCLASS_ABBR=='RigidGroup'", 11: 'force', 12: 0}
Acp_12={1: 12, 2: 'mod.AroCore.acp.AcpSum', 3: [329, 412], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (13, 1)}, 7: {2: [(11, 1)]}, 8: 'New Acp', 9: '', 10: "AROCLASS_ABBR=='RigidGroup'", 11: 'force', 12: 0}
Acp_13={1: 13, 2: 'mod.AroCore.acp.AcpSelector', 3: [498, 414], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(12, 1)]}, 8: 'f_MP', 9: '', 10: "AROVE['AroID'] in SELF_ARO.children", 11: 'force', 12: 0}
Acp_14={1: 14, 2: 'mod.AroCore.acp.AcpProvider', 3: [171, 577], 4: 'Both', 5: {1: 'in'}, 6: {1: (16, 2)}, 7: {}, 8: 'f_MP', 9: '', 10: "AROCLASS_ABBR=='MassPoint'", 11: 'force', 12: 0}
Acp_15={1: 15, 2: 'mod.AroCore.acp.AcpSelector', 3: [497, 579], 4: 'Both', 5: {1: 'out'}, 6: {}, 7: {1: [(16, 1)]}, 8: 'fSlctr', 9: '', 10: "SELF_ARO.AroID in ARO.targets and ARO.tag=='force'", 11: 'value', 12: [0, 0, 0]}
Acp_16={1: 16, 2: 'mod.AroCore.acp.AcpSum', 3: [332, 579], 4: 'Both', 5: {1: 'in', 2: 'out'}, 6: {1: (15, 1)}, 7: {2: [(14, 1)]}, 8: 'New Acp', 9: '', 10: "SELF_ARO.AroID in ARO.targets and ARO.tag=='force'", 11: 'value', 12: [0, 0, 0]}
