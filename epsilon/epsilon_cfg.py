import epsilon_sim as sim

class Numeric:
	def aa(self):
		return


class Variable (Numeric):
	def __init__(self,name,parent_function):
		assert(isinstance(name,str))
		assert(isinstance(parent_function,Function))
		self.name = name
		self.parent_function = parent_function
		return


class Constant (Numeric):
	def __init__(self,value,parent_function):
		assert(isinstance(value,int))
		assert(isinstance(parent_function,Function))
		self.value = value
		self.name = value
		self.parent_function = parent_function


class Instruction:
	def __init__(self,parent_basicblock):
		assert(isinstance(parent_basicblock,BasicBlock))
		self.parent_basicblock = parent_basicblock
		return
	
	def show(self):
		return

class CmpInstruction (Instruction):

	def update(self,lhs,rhs_1,rhs_2,op):
		assert(op.is_operation('<') or op.is_operation('>') or op.is_operation('<=') or op.is_operation('>=') or op.is_operation('==') or op.is_operation('!='))
		assert(isinstance(lhs,Variable) and isinstance(rhs_1,Numeric) and isinstance(rhs_2,Numeric))
		self.lhs = lhs
		self.rhs_1 = rhs_1
		self.rhs_2 = rhs_2
		self.op = op
		return

	def show(self):
		print self.lhs.name,' = ',self.rhs_1.name,' ',self.op.name,' ',self.rhs_2.name
		return

class ArithInstruction(Instruction):

	def update(self,lhs,rhs_1,rhs_2,op):
		assert(op.is_operation('+') or op.is_operation('*') or op.is_operation('/') or op.is_operation('-') or op.is_operation('%'))
		assert(isinstance(lhs,Variable) and isinstance(rhs_1,Numeric) and isinstance(rhs_2,Numeric))
		self.lhs = lhs
		self.rhs_1 = rhs_1
		self.rhs_2 = rhs_2
		self.op = op
		return
	
	def show(self):
		print self.lhs.name,' = ',self.rhs_1.name,' ',self.op.name,' ',self.rhs_2.name
		return
	
	def get_sim(self):
		return


class EqInstruction (Instruction):
	
	def update(self,lhs,rhs):
		assert(isinstance(lhs,Variable) and isinstance(rhs,Numeric))
		self.lhs = lhs
		self.rhs = rhs
		return

	def show(self):
		print self.lhs.name,' = ', self.rhs.name
		return

class Operation:
	def __init__(self,name):
		self.name = name
		return

	def is_operation(self,op_name):
		if self.name == op_name:
			return True
		else:
			return False

class BasicBlock:
	def __init__(self,parent_function):
		assert(isinstance(parent_function,Function))
		self.instruction_list = []
		parent_function.add_basicblock(self)
		self.parent_function = parent_function
		self.child_true = None
		self.child_false = None
		self.number_of_instructions = 0
		self.used_variables = []
		self.defined_variables = []
		return
	
	def add_instruction (self,instr):
		assert(isinstance(instr,Instruction))
		self.number_of_instructions += 1
		self.instruction_list.append(instr)
		if instr.lhs not in self.defined_variables:
			if isinstance(instr.lhs,Variable):
				self.defined_variables.append(instr.lhs)
		if isinstance(instr,EqInstruction):
			if isinstance(instr.rhs,Variable):
				if instr.rhs not in self.used_variables:
					self.used_variables.append(instr.rhs)
		else:
			if isinstance(instr.rhs_1,Variable):
				if instr.rhs_1 not in self.used_variables:
					self.used_variables.append(instr.rhs_1)
			if isinstance(instr.rhs_2,Variable):
				if instr.rhs_2 not in self.used_variables:
					self.used_variables.append(instr.rhs_2)
			
		return

	def set_child_true(self,bb):
		assert(isinstance(bb,BasicBlock))
		self.child_true = bb
		return

	def set_child_false(self,bb):
		assert(isinstance(bb,BasicBlock))
		self.child_false = bb
		return
	
	def set_condition(self,condition,condition_instr):
		assert(isinstance(condition,Numeric))
		assert(isinstance(condition_instr,CmpInstruction) or (condition_instr==None))
		self.condition = condition
		self.condition_instr = condition_instr
		if condition_instr is not None:
			if condition_instr.lhs not in self.defined_variables:
				if isinstance(condition_instr.lhs,Variable):
					self.defined_variables.append(condition_instr.lhs)
			if isinstance(condition_instr.rhs_1,Variable):
				if condition_instr.rhs_1 not in self.used_variables:
					self.used_variables.append(condition_instr.rhs_1)
			if isinstance(condition_instr.rhs_2,Variable):
				if condition_instr.rhs_2 not in self.used_variables:
					self.used_variables.append(condition_instr.rhs_2)
		
	def clean_up(self):
		if self.child_true == self.child_false:
			self.child = self.child_true
			if(self.child == None):
				self.number_of_children = 0
			else:
				self.number_of_children = 1
		else:
			self.number_of_children = 2
	
	def set_id(self,identity):
		self.identity = identity
	
	def show(self):
		if self.number_of_children is 0:
			print 'BasicBlock',self.identity
		elif self.number_of_children is 1:
			print 'BasicBlock',self.identity,':: child =',self.child.identity
		elif self.number_of_children is 2:
			print 'BasicBlock',self.identity,':: child_true =',self.child_true.identity,' | child_false = ',self.child_false.identity,'| condition = ',self.condition.name
		for inst in self.instruction_list:
			inst.show()
		if self.number_of_children is 2:
			if not self.condition_instr == None:
				self.condition_instr.show()
		print '\n'
			
			

class Function:
	def __init__(self):
		self.basicblock_list = []
		self.variable_list = []
		self.input_variable_list = []
		self.output_variable_list = []
	
		return
	
	def add_basicblock(self,bb):
		assert(isinstance(bb,BasicBlock))
		self.basicblock_list.append(bb)

	def clean_up(self):
		identity = 0
		for bb in self.basicblock_list:
			bb.clean_up()
			bb.set_id(identity)
			identity += 1
		return

	def show(self):
		for bb in self.basicblock_list:
			bb.show()
	
	def add_variable(self,var):
		assert(isinstance(var,Variable))
		self.variable_list.append(var)
	
	def get_variable_or_constant(self,numeric):
		assert(isinstance(numeric,str) or isinstance(numeric,int))
		if isinstance(numeric,str):
			for v in self.variable_list:
				if v.name == numeric:
					return v
			new_v = Variable(numeric,self)
			self.add_variable(new_v)
			return new_v
		else:
			new_c = Constant(numeric,self)
			return new_c
	
	def add_input_variable(self,var):
		assert(isinstance(var,Variable))
		self.input_variable_list.append(var)

	def add_output_variable(self,var):
		assert(isinstance(var,Variable))
		self.output_variable_list.append(var)
	
	def add_summary(self,summary_string):
		assert(isinstance(summary_string,str))
		self.summary = summary_string
		return
