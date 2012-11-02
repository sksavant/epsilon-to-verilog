import eps_grammar
import cfg


class Node:
	def __init__(self):
		return

class ExprNode(Node):
	def __init__(self):
		return

class StmtNode(Node):
	def __init__(self):
		return

class SingleExprNode(ExprNode):
	def __init__(self):
		return

class SummaryNode:
	def __init__(self,sentence):
		assert(isinstance(sentence,str))
		self.sentence = sentence
		return

class BinExprNode(ExprNode):
	def __init__(self,operator,operand_1,operand_2):
		'''operand_1 and operand_2 are instances of SingleExpr'''
		assert(isinstance(operator,str))
		assert(isinstance(operand_1,SingleExprNode))
		assert(isinstance(operand_2,SingleExprNode))
		self.operator = operator
		self.operand_1 = operand_1
		self.operand_2 = operand_2
	
	def show(self,n):
		assert(isinstance(n,int))
		print   n , '[label="',self.operator,'"]'
		print   n , ' -- ', n+1
		print   n , ' -- ', n+2
		self.operand_1.show(n+1)
		self.operand_2.show(n+2)
		return n+3

class VariableNode(SingleExprNode):
	def __init__(self,name):
		assert(isinstance(name,str))
		self.name = name

	def show(self,n):
		assert(isinstance(n,int))
		print n , '[label="',self.name,'"]'
		return n+1

class NumberNode(SingleExprNode):
	def __init__(self,number):
		assert(isinstance(number,int))
		self.number = number
		self.name = number

	def show(self,n):
		assert(isinstance(n,int))
		print   n , '[label="',self.number,'"]'
		return n+1

class ArithExprNode(BinExprNode):
	def __init__(self,operator,operand_1,operand_2):
		BinExprNode.__init__(self,operator,operand_1,operand_2)

class CmpExprNode(BinExprNode):
	def __init__(self,operator,operand_1,operand_2):
		BinExprNode.__init__(self,operator,operand_1,operand_2)

class EqNode(StmtNode):
	def __init__(self,variable,expr):
		assert(isinstance(variable,VariableNode))
		assert(isinstance(expr,ExprNode))
		self.variable = variable
		self.expr = expr
		return

	
	def process_cfg(self,bb):
		assert(isinstance(bb,cfg.BasicBlock))
		result = bb.parent_function.get_variable_or_contant(self.variable.name)
		if isinstance(self.expr,SingleExprNode):
			if isinstance(self.expr,NumberNode):
				operand = cfg.Constant(self.expr.number,bb.parent_function)
			else:
				operand = bb.parent_function.get_variable_or_contant(self.expr.name)
			instr = cfg.EqInstruction(bb)
			instr.update(result,operand)
			bb.add_instruction(instr)
		else:
			if isinstance(self.expr.operand_1,NumberNode):
				operand_1 = cfg.Constant(self.expr.operand_1.number,bb.parent_function)
			else:
				operand_1 = bb.parent_function.get_variable_or_contant(self.expr.operand_1.name)
			if isinstance(self.expr.operand_2,NumberNode):
				operand_2 = cfg.Constant(self.expr.operand_2.number,bb.parent_function)
			else:
				operand_2 = bb.parent_function.get_variable_or_contant(self.expr.operand_2.name)
			if (isinstance(self.expr,CmpExprNode)):
				instr = cfg.CmpInstruction(bb)
				op = cfg.Operation(self.expr.operator)
				instr.update(result,operand_1,operand_2,op)
			else:
				instr = cfg.ArithInstruction(bb)
				op = cfg.Operation(self.expr.operator)
				instr.update(result,operand_1,operand_2,op)
			bb.add_instruction(instr)


					
				
		return bb

	def show(self,n):
		assert(isinstance(n,int))
		print   n , '[label="="]'
		print   n , ' -- ',n+1
		print   n , ' -- ',n+2
		self.variable.show(n+1)
		k = self.expr.show(n+2)
		return k


class WhileNode(StmtNode):
	def __init__(self,condition,body):
		assert(isinstance(condition,SingleExprNode) or isinstance(condition,CmpExprNode))
		self.condition = condition
		self.body = body
		for stmt in body:
			assert(isinstance(stmt,StmtNode))

	def process_cfg(self,bb_old):
		assert(isinstance(bb_old,cfg.BasicBlock))
		if isinstance(self.condition,VariableNode):
			condn = bb_old.parent_function.get_variable_or_contant(self.condition.name)
			condn_instr = None
		elif isinstance(self.condition,CmpExprNode):
			condn = bb_old.parent_function.get_variable_or_contant('x')
			condn_instr = cfg.CmpInstruction(bb_old)
			rhs_1 = bb_old.parent_function.get_variable_or_contant(self.condition.operand_1.name)
			rhs_2 = bb_old.parent_function.get_variable_or_contant(self.condition.operand_2.name)
			op = cfg.Operation(self.condition.operator)
			condn_instr.update(condn,rhs_1,rhs_2,op)
		bb_old.set_condition(condn,condn_instr)
		bb_new = cfg.BasicBlock(bb_old.parent_function)
		bb_old.set_child_false(bb_new)
		bb_body = cfg.BasicBlock(bb_old.parent_function)
		bb_old.set_child_true(bb_body)
		bb_temp = bb_body
		for stmt in self.body:
			bb_temp = stmt.process_cfg(bb_temp)
		bb_temp.set_child_true(bb_body)
		bb_temp.set_child_false(bb_new)
		bb_temp.set_condition(condn,condn_instr)
		return bb_new

	def show(self,n):
		assert(isinstance(n,int))
		print   n,'[label="while"]'
		print   n,'[color="red"]'
		print 	n+1,'[label="condn"]'
		print   n+1,'[color="red"]'
		print   n+1,'[shape="box"]'
		print   n+2,'[label="body"]'
		print   n+2,'[color="red"]'
		print   n+2,'[shape="box"]'
		print   n,' -- ',n+1
		print   n,' -- ',n+2
		print   n+1,' -- ',n+3
		self.condition.show(n+3)
		index = n+4
		for stmt in self.body:
			print  n+2,'--',index
			index = stmt.show(index)
		return index

class IfElseNode(StmtNode):
	def __init__(self,condition,body_yes,body_no):
		assert(isinstance(condition,SingleExprNode) or isinstance(condition,CmpExprNode))
		self.condition = condition
		self.body_yes = body_yes
		self.body_no = body_no
		for stmt in body_yes:
			assert(isinstance(stmt,StmtNode))
		for stmt in body_no:
			assert(isinstance(stmt,StmtNode))

	def process_cfg(self,bb_old):
		assert(isinstance(bb_old,cfg.BasicBlock))
		if isinstance(self.condition,VariableNode):
			condn = bb_old.parent_function.get_variable_or_contant(self.condition.name)
			condn_instr = None
		elif isinstance(self.condition,CmpExprNode):
			condn = bb_old.parent_function.get_variable_or_contant('x')
			condn_instr = cfg.CmpInstruction(bb_old)
			rhs_1 = bb_old.parent_function.get_variable_or_contant(self.condition.operand_1.name)
			rhs_2 = bb_old.parent_function.get_variable_or_contant(self.condition.operand_2.name)
			op = cfg.Operation(self.condition.operator)
			condn_instr.update(condn,rhs_1,rhs_2,op)
		bb_old.set_condition(condn,condn_instr)
		bb_new = cfg.BasicBlock(bb_old.parent_function)
		bb_body_yes = cfg.BasicBlock(bb_old.parent_function)
		bb_body_no = cfg.BasicBlock(bb_old.parent_function)
		bb_old.set_child_true(bb_body_yes)
		bb_old.set_child_false(bb_body_no)
		bb_temp_yes = bb_body_yes
		bb_temp_no = bb_body_no
		for stmt in self.body_yes:
			bb_temp_yes = stmt.process_cfg(bb_temp_yes)
		for stmt in self.body_no:
			bb_temp_no = stmt.process_cfg(bb_temp_no)
		bb_temp_yes.set_child_false(bb_new)
		bb_temp_yes.set_child_true(bb_new)
		bb_temp_no.set_child_false(bb_new)
		bb_temp_no.set_child_true(bb_new)
		return bb_new

	def show(self,n):
		assert(isinstance(n,int))
		print   n,'[label="if-else"]'
		print   n,'[color="blue"]'
		print   n+1,'[label="condn"]'
		print   n+1,'[color="blue"]'
		print   n+1,'[shape="box"]'
		print   n+2,'[label="body_yes"]'
		print   n+2,'[color="blue"]'
		print   n+2,'[shape="box"]'
		print   n+3,'[label="body_no"]'
		print   n+3,'[color="blue"]'
		print   n+3,'[shape="box"]'
		print   n,' -- ',n+1
		print   n,' -- ',n+2
		print   n,' -- ',n+3
		print   n+1,' -- ',n+4
		self.condition.show(n+4)
		index = n+5
		for stmt in self.body_yes:
			print   n+2,'--',index
			index = stmt.show(index)
		for stmt in self.body_no:
			print   n+3,'--',index
			index = stmt.show(index)
		return index
	
class IfNode(StmtNode):
	def __init__(self,condition,body):
		assert(isinstance(condition,SingleExprNode) or isinstance(condition,CmpExprNode))
		self.condition = condition
		self.body = body
		for stmt in body:
			assert(isinstance(stmt,StmtNode))

	def process_cfg(self,bb_old):
		assert(isinstance(bb_old,cfg.BasicBlock))
		if isinstance(self.condition,VariableNode):
			condn = bb_old.parent_function.get_variable_or_contant(self.condition.name)
			condn_instr = None
		elif isinstance(self.condition,CmpExprNode):
			condn = bb_old.parent_function.get_variable_or_contant('x')
			condn_instr = cfg.CmpInstruction(bb_old)
			rhs_1 = bb_old.parent_function.get_variable_or_contant(self.condition.operand_1.name)
			rhs_2 = bb_old.parent_function.get_variable_or_contant(self.condition.operand_2.name)
			op = cfg.Operation(self.condition.operator)
			condn_instr.update(condn,rhs_1,rhs_2,op)
		bb_old.set_condition(condn,condn_instr)
		bb_new = cfg.BasicBlock(bb_old.parent_function)
		bb_old.set_child_false(bb_new)
		bb_body = cfg.BasicBlock(bb_old.parent_function)
		bb_old.set_child_true(bb_body)
		bb_temp = bb_body
		for stmt in self.body:
			bb_temp = stmt.process_cfg(bb_temp)
		bb_temp.set_child_true(bb_new)
		bb_temp.set_child_false(bb_new)
		return bb_new
	
	def show(self,n):
		assert(isinstance(n,int))
		print   n,'[label="if"]'
		print   n,'[color="green"]'
		print   n+1,'[label="condn"]'
		print   n+1,'[color="green"]'
		print   n+1,'[shape="box"]'
		print   n+2,'[label="body"]'
		print   n+2,'[color="green"]'
		print   n+2,'[shape="box"]'
		print   n,' -- ',n+1
		print   n,' -- ',n+2
		print   n+1,' -- ',n+3
		self.condition.show(n+3)
		index = n+4
		for stmt in self.body:
			print   n+2,'--',index
			index = stmt.show(index)
		return index

class Function(Node):
	def __init__(self,input_variable_list,output_variable_list,body):
		self.body = body
		self.input_variable_list = input_variable_list
		self.output_variable_list = output_variable_list
		for var in input_variable_list:
			assert(isinstance(var,VariableNode))
		for var in output_variable_list:
			assert(isinstance(var,VariableNode))
		for stmt in body:
			assert(isinstance(stmt,StmtNode))

	def add_summary(self,summary):
		assert(isinstance(summary,SummaryNode))
		self.summary = summary
		return
	
	def get_cfg(self):
		cfg_function = cfg.Function()
		for ast_var in self.input_variable_list:
			cfg_var = cfg_function.get_variable_or_contant(ast_var.name)
			cfg_function.add_input_variable(cfg_var)
		for ast_var in self.output_variable_list:
			cfg_var = cfg_function.get_variable_or_contant(ast_var.name)
			cfg_function.add_output_variable(cfg_var)
		bb_start  = cfg.BasicBlock(cfg_function)
		bb_temp = bb_start
		for stmt in self.body:
			bb_temp = stmt.process_cfg(bb_temp)
		cfg_function.clean_up()
		cfg_function.add_summary(self.summary.sentence)
		return cfg_function

	def show(self):
		print   "graph AST {"
		print   '0[label="function"]'
		print   '1[label="inputs"]'
		print   '2[label="outputs"]'
		print   '3[label="body"]'
		print   '0 -- 1'
		print   '0 -- 2'
		print   '0 -- 3'
		
		index = 4
		for var in self.input_variable_list:
			print 1, '--',index
			index = var.show(index)
		for var in self.output_variable_list:
			print  2, '--',index
			index = var.show(index)
		for stmt in self.body:
			print  3,'--',index
			index = stmt.show(index)
		print  "}"
	
