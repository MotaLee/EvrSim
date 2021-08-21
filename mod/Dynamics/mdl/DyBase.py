ACP_INDEX=[1, 2, 3]
Acp_1={1: 1, 2: 'Acp_1', 3: [632, 205], 4: '', 5: True, 6: False, 7: ('Dynamics', 'DyBase'), 8: 'core.esc.acp.AcpGetter', 9: "ABBRCLASS=='Beam2D'", 10: [{'io': 'out', 'pid': 1, 'name': 'ptf', 'link': [(3, 1)]}, {'io': 'out', 'pid': 2, 'name': 'pts', 'link': [(3, 2)]}]}
Acp_2={1: 2, 2: 'Acp_2', 3: [200, 200], 4: '', 5: False, 6: True, 7: ('Dynamics', 'DyBase'), 8: 'core.esc.acp.AcpSetter', 9: "ABBRCLASS=='Beam2D'", 10: [{'io': 'in', 'pid': 1, 'name': 'position', 'link': [(3, 0)]}]}
Acp_3={1: 3, 2: 'Acp_3', 3: [397, 204], 4: '', 5: False, 6: True, 7: ('Dynamics', 'DyBase'), 8: 'core.esc.acp.AcpMean', 10: [{'io': 'out', 'pid': 0, 'name': 'Out', 'link': [(2, 1)]}, {'io': 'in', 'pid': 1, 'name': 'In 1', 'link': [(1, 1)]}, {'io': 'in', 'pid': 2, 'name': 'In 2', 'link': [(1, 2)]}]}
KEY_DICT={'acpid': 1, 'acp_name': 2, 'position': 3, 'desc': 4, 'fix_in': 5, 'fix_out': 6, 'mdl': 7, 'AcpClass': 8, 'expression': 9, 'port': 10}
