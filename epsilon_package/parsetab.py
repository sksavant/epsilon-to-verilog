
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xf7\xf5\x15o\xdf9\xc1EA\xb85\x06\x88\nk\x1a'
    
_lr_action_items = {'RETURN':([10,11,12,13,18,23,25,27,49,50,55,56,60,],[-7,-2,17,-7,-6,-9,-8,-12,-13,-14,-26,-27,-28,]),'SUB':([23,25,27,],[-9,-8,40,]),'EQEQ':([23,24,25,27,],[-9,33,-8,33,]),'NUMBER':([19,20,21,30,31,32,33,34,35,36,38,39,40,41,42,43,44,],[23,23,23,23,-16,-18,-19,-15,-17,-20,23,23,-24,-22,-23,-25,-21,]),'LCURLY':([8,37,45,57,],[9,48,51,58,]),'WHILE':([10,11,13,23,25,27,48,49,50,51,55,56,58,60,],[14,-2,14,-9,-8,-12,14,-13,-14,14,-26,-27,14,-28,]),'MUL':([23,25,27,],[-9,-8,41,]),'DIV':([23,25,27,],[-9,-8,42,]),'NEQ':([23,24,25,27,],[-9,36,-8,36,]),'RCURLY':([13,18,23,25,27,46,48,49,50,51,53,54,55,56,58,59,60,],[-7,-6,-9,-8,-12,52,-7,-13,-14,-7,55,56,-26,-27,-7,60,-28,]),'LT':([23,24,25,27,],[-9,34,-8,34,]),'$end':([1,3,52,],[-1,0,-3,]),'FUNCTION':([0,],[2,]),'GT':([23,24,25,27,],[-9,31,-8,31,]),'GTE':([23,24,25,27,],[-9,32,-8,32,]),'EQUALS':([15,],[20,]),'SUMMARY':([9,],[11,]),'ADD':([23,25,27,],[-9,-8,44,]),'LTE':([23,24,25,27,],[-9,35,-8,35,]),'VAR':([4,5,10,11,13,19,20,21,22,23,25,27,30,31,32,33,34,35,36,38,39,40,41,42,43,44,48,49,50,51,55,56,58,60,],[5,5,15,-2,15,25,25,25,5,-9,-8,-12,25,-16,-18,-19,-15,-17,-20,25,25,-24,-22,-23,-25,-21,15,-13,-14,15,-26,-27,15,-28,]),'ELSE':([56,],[57,]),'IF':([10,11,13,23,25,27,48,49,50,51,55,56,58,60,],[16,-2,16,-9,-8,-12,16,-13,-14,16,-26,-27,16,-28,]),'LROUND':([2,14,16,17,],[4,19,21,22,]),'RROUND':([4,5,6,7,22,23,24,25,26,28,29,47,],[-5,-5,8,-4,-5,-9,-11,-8,37,45,46,-10,]),'MOD':([23,25,27,],[-9,-8,43,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'function':([0,],[1,]),'stmt_list':([10,13,48,51,58,],[12,18,53,54,59,]),'comparison_op':([24,27,],[30,38,]),'stmt':([10,13,48,51,58,],[13,13,13,13,13,]),'summary':([9,],[10,]),'arithmetic_op':([27,],[39,]),'program':([0,],[3,]),'value':([19,20,21,30,38,39,],[24,27,24,47,49,50,]),'var_list':([4,5,22,],[6,7,29,]),'condn':([19,21,],[26,28,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> function','program',1,'p_program','/home/anay/codes/epsilon/source/eps_grammar.py',7),
  ('summary -> SUMMARY','summary',1,'p_summary','/home/anay/codes/epsilon/source/eps_grammar.py',12),
  ('function -> FUNCTION LROUND var_list RROUND LCURLY summary stmt_list RETURN LROUND var_list RROUND RCURLY','function',12,'p_function','/home/anay/codes/epsilon/source/eps_grammar.py',16),
  ('var_list -> VAR var_list','var_list',2,'p_var_list','/home/anay/codes/epsilon/source/eps_grammar.py',21),
  ('var_list -> <empty>','var_list',0,'p_var_list_empty','/home/anay/codes/epsilon/source/eps_grammar.py',27),
  ('stmt_list -> stmt stmt_list','stmt_list',2,'p_stmt_list','/home/anay/codes/epsilon/source/eps_grammar.py',32),
  ('stmt_list -> <empty>','stmt_list',0,'p_stmt_list_empty','/home/anay/codes/epsilon/source/eps_grammar.py',38),
  ('value -> VAR','value',1,'p_value_var','/home/anay/codes/epsilon/source/eps_grammar.py',43),
  ('value -> NUMBER','value',1,'p_value_number','/home/anay/codes/epsilon/source/eps_grammar.py',48),
  ('condn -> value comparison_op value','condn',3,'p_condn_expr','/home/anay/codes/epsilon/source/eps_grammar.py',53),
  ('condn -> value','condn',1,'p_condn_value','/home/anay/codes/epsilon/source/eps_grammar.py',58),
  ('stmt -> VAR EQUALS value','stmt',3,'p_stmt_eq','/home/anay/codes/epsilon/source/eps_grammar.py',64),
  ('stmt -> VAR EQUALS value comparison_op value','stmt',5,'p_stmt_cmp_eq','/home/anay/codes/epsilon/source/eps_grammar.py',69),
  ('stmt -> VAR EQUALS value arithmetic_op value','stmt',5,'p_stmt_ariarithh_eq','/home/anay/codes/epsilon/source/eps_grammar.py',74),
  ('comparison_op -> LT','comparison_op',1,'p_comparison','/home/anay/codes/epsilon/source/eps_grammar.py',80),
  ('comparison_op -> GT','comparison_op',1,'p_comparison','/home/anay/codes/epsilon/source/eps_grammar.py',81),
  ('comparison_op -> LTE','comparison_op',1,'p_comparison','/home/anay/codes/epsilon/source/eps_grammar.py',82),
  ('comparison_op -> GTE','comparison_op',1,'p_comparison','/home/anay/codes/epsilon/source/eps_grammar.py',83),
  ('comparison_op -> EQEQ','comparison_op',1,'p_comparison','/home/anay/codes/epsilon/source/eps_grammar.py',84),
  ('comparison_op -> NEQ','comparison_op',1,'p_comparison','/home/anay/codes/epsilon/source/eps_grammar.py',85),
  ('arithmetic_op -> ADD','arithmetic_op',1,'p_arithmetic','/home/anay/codes/epsilon/source/eps_grammar.py',90),
  ('arithmetic_op -> MUL','arithmetic_op',1,'p_arithmetic','/home/anay/codes/epsilon/source/eps_grammar.py',91),
  ('arithmetic_op -> DIV','arithmetic_op',1,'p_arithmetic','/home/anay/codes/epsilon/source/eps_grammar.py',92),
  ('arithmetic_op -> SUB','arithmetic_op',1,'p_arithmetic','/home/anay/codes/epsilon/source/eps_grammar.py',93),
  ('arithmetic_op -> MOD','arithmetic_op',1,'p_arithmetic','/home/anay/codes/epsilon/source/eps_grammar.py',94),
  ('stmt -> WHILE LROUND condn RROUND LCURLY stmt_list RCURLY','stmt',7,'p_stmt_while','/home/anay/codes/epsilon/source/eps_grammar.py',100),
  ('stmt -> IF LROUND condn RROUND LCURLY stmt_list RCURLY','stmt',7,'p_stmt_if','/home/anay/codes/epsilon/source/eps_grammar.py',105),
  ('stmt -> IF LROUND condn RROUND LCURLY stmt_list RCURLY ELSE LCURLY stmt_list RCURLY','stmt',11,'p_stmt_ifelse','/home/anay/codes/epsilon/source/eps_grammar.py',110),
]
