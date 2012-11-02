import ply.yacc as yacc
import eps_lexer
import ast
tokens = eps_lexer.tokens

def p_program(p):
	'''program : function '''
	#print '''program : function'''
	p[0] = p[1]

def p_summary(p):
	'''summary : SUMMARY'''
	p[0] = ast.SummaryNode(p[1])

def p_function(p):
	'''function : FUNCTION LROUND var_list RROUND LCURLY summary stmt_list RETURN LROUND var_list RROUND RCURLY'''
	#print '''function : FUNCTION LROUND var_list RROUND LCURLY stmt_list RETURN LROUND var_list RROUND RCURLY'''
	p[0] = ast.Function(p[3],p[10],p[7])
	p[0].add_summary(p[6])

def p_var_list(p):
	'''var_list : VAR var_list'''
	#print '''var_list : VAR var_list'''
	p[0] = p[2]
	p[0].insert(0,ast.VariableNode(p[1]))

def p_var_list_empty(p):
	'''var_list : '''
	#print '''var_list : '''
	p[0] = []

def p_stmt_list(p):
	'''stmt_list : stmt stmt_list'''
	#print '''stmt_list : stmt stmt_list'''
	p[0] = p[2]
	p[0].insert(0,p[1])

def p_stmt_list_empty(p):
	'''stmt_list : '''
	#print '''stmt_list : '''
	p[0] = []

def p_value_var(p):
	'''value : VAR'''
	#print '''stmt_list : '''
	p[0] = ast.VariableNode(p[1])

def p_value_number(p):
	'''value : NUMBER'''
	#print '''value : NUMBER'''
	p[0] = ast.NumberNode(p[1])

def p_condn_expr(p):
	'''condn : value comparison_op value'''
	#print '''condn : value comparison_op value'''
	p[0] = ast.CmpExprNode(p[2],p[1],p[3])

def p_condn_value(p):
	'''condn : value'''
	#print '''condn : value'''
	p[0] = p[1]
	

def p_stmt_eq(p):
	'''stmt : VAR EQUALS value'''
	#print '''stmt : VAR EQUALS value'''
	p[0] = ast.EqNode(ast.VariableNode(p[1]),p[3])

def p_stmt_cmp_eq(p):
	'''stmt : VAR EQUALS value comparison_op value'''
	#print '''stmt : VAR EQUALS value comparison_op value'''
	p[0] = ast.EqNode(ast.VariableNode(p[1]),ast.CmpExprNode(p[4],p[3],p[5]))

def p_stmt_ariarithh_eq(p):
	'''stmt : VAR EQUALS value arithmetic_op value'''
	#print '''stmt : VAR EQUALS value arithmetic_op value'''
	p[0] = ast.EqNode(ast.VariableNode(p[1]),ast.ArithExprNode(p[4],p[3],p[5]))


def p_comparison(p):
	'''comparison_op : LT
			  | GT
			  | LTE
			  | GTE
			  | EQEQ
			  | NEQ'''
	#print '''comparison_op : '''
	p[0] = p[1]

def p_arithmetic(p):
	'''arithmetic_op : ADD
				 | MUL
				 | DIV
				 | SUB
				 | MOD'''
	#print '''arithmetic_op : ..'''
	p[0] = p[1]
	

def p_stmt_while(p):
	'''stmt : WHILE LROUND condn RROUND LCURLY stmt_list RCURLY'''
	#print '''stmt : WHILE LROUND condn RROUND LCURLY stmt_list RCURLY'''
	p[0] = ast.WhileNode(p[3],p[6])

def p_stmt_if(p):
	'''stmt : IF LROUND condn RROUND LCURLY stmt_list RCURLY'''
	#print '''stmt : IF LROUND condn RROUND LCURLY stmt_list RCURLY'''
	p[0] = ast.IfNode(p[3],p[6])

def p_stmt_ifelse(p):
	'''stmt : IF LROUND condn RROUND LCURLY stmt_list RCURLY ELSE LCURLY stmt_list RCURLY'''
	#print '''stmt : IF LROUND condn RROUND LCURLY stmt_list RCURLY ELSE LCURLY stmt_list RCURLY'''
	p[0] = ast.IfElseNode(p[3],p[6],p[10])

def p_error(p):
	print "incorrect grammar ... exiting"
	quit()


# def_ast is the only function that should be used by the outside world to access the grammar of this file

def get_ast(data):
	yacc.yacc()
	return yacc.parse(data)
