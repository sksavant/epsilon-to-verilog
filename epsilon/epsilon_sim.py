# assert that all instructions being passed to different functions are of the right class

#########
class Instruction:
	def __init__(self,parent_function):
		assert(isinstance(parent_function,Function))
		self.parent_function = parent_function
		return
	
	def set_label(self,label):
		self.label = label

########
class ExecutableInstruction (Instruction):
	
	def execute(self):
		return

class JumpInstruction (Instruction):

	def get_next_instr(self):
		return

class ReturnInstruction (Instruction):
	
	def show(self):
		print self.label, ':  ','return'
		return
########
class UncondnJumpInstruction (JumpInstruction):
	
	def update(self,next_instr_label):
		assert(isinstance(next_instr_label,int))
		self.next_instr_label = next_instr_label
		return
	
	def get_next_instr(self):
		return self.next_instr_label
	
	def show(self):
		print self.label, ':  ','branch ',self.next_instr_label
		return

########

class CondnJumpInstruction (JumpInstruction):
	
	def update(self,cond_var,instr_true_label,instr_false_label):
		assert(isinstance(instr_true_label,int) and isinstance(instr_false_label,int))
		assert(isinstance(cond_var,Variable))
		self.cond_var = cond_var
		self.instr_true_label = instr_true_label
		self.instr_false_label = instr_false_label
		return
	
	def get_next_instr(self):
		if self.cond_var.value is 0:
			return self.instr_false_label
		else:
			return self.instr_true_label
	
	def show(self):
		print self.label, ':  ','branch (',self.cond_var.name,') | ',self.instr_true_label,',',self.instr_false_label
		return

	

########
class EqInstruction (ExecutableInstruction):
	
	def update(self,lhs,rhs):
		assert(isinstance(lhs,Variable) and isinstance(rhs,Num))
		self.lhs = lhs
		self.rhs = rhs
		return

	def execute(self):
		self.lhs.value = self.rhs.value
		return
	
	def show(self):
		print self.label, ':  ',self.lhs.name,' = ', self.rhs.name

########
class CmpInstruction (ExecutableInstruction):

	def update(self,lhs,rhs_1,rhs_2,op):
		assert(op.is_operation('<') or op.is_operation('>') or op.is_operation('<=') or op.is_operation('>=') or op.is_operation('==') or op.is_operation('!='))
		assert(isinstance(lhs,Variable) and isinstance(rhs_1,Num) and isinstance(rhs_2,Num))
		self.lhs = lhs
		self.rhs_1 = rhs_1
		self.rhs_2 = rhs_2
		self.op = op
		return

	def execute(self):
		if self.op.is_operation('<'):
			if self.rhs_1.value < self.rhs_2.value:
				self.lhs.value = 1
			else:
				self.lhs.value = 0
		elif self.op.is_operation('>'):
			if self.rhs_1.value > self.rhs_2.value:
				self.lhs.value = 1
			else:
				self.lhs.value = 0
		elif self.op.is_operation('<='):
			if self.rhs_1.value <= self.rhs_2.value:
				self.lhs.value = 1
			else:
				self.lhs.value = 0
		elif self.op.is_operation('>='):
			if self.rhs_1.value >= self.rhs_2.value:
				self.lhs.value = 1
			else:
				self.lhs.value = 0
		elif self.op.is_operation('=='):
			if self.rhs_1.value == self.rhs_2.value:
				self.lhs.value = 1
			else:
				self.lhs.value = 0
		elif self.op.is_operation('!='):
			if self.rhs_1.value != self.rhs_2.value:
				self.lhs.value = 1
			else:
				self.lhs.value = 0
		return

	def show(self):
		print self.label, ':  ',self.lhs.name,' = ',self.rhs_1.name,' ',self.op.name,' ',self.rhs_2.name
		return

########
class ArithInstruction(ExecutableInstruction):

	def update(self,lhs,rhs_1,rhs_2,op):
		assert(op.is_operation('+') or op.is_operation('*') or op.is_operation('/') or op.is_operation('-') or op.is_operation('%'))
		assert(isinstance(lhs,Variable) and isinstance(rhs_1,Num) and isinstance(rhs_2,Num))
		self.lhs = lhs
		self.rhs_1 = rhs_1
		self.rhs_2 = rhs_2
		self.op = op
		return

	def execute(self):
		if self.op.is_operation('+'):
			self.lhs.value = self.rhs_1.value + self.rhs_2.value
		elif self.op.is_operation('*'):
			self.lhs.value = self.rhs_1.value * self.rhs_2.value
		elif self.op.is_operation('/'):
			self.lhs.value = self.rhs_1.value / self.rhs_2.value
		elif self.op.is_operation('-'):
			self.lhs.value = self.rhs_1.value - self.rhs_2.value
		elif self.op.is_operation('%'):
			self.lhs.value = self.rhs_1.value % self.rhs_2.value
		return
	
	def show(self):
		print self.label, ':  ',self.lhs.name,' = ',self.rhs_1.name,' ',self.op.name,' ',self.rhs_2.name
		return

########
class Num:
	def aa(self):
		return

########

class Variable(Num):
	def __init__(self,name):
		self.value = 0
		self.name = name
		return

	def set_name(self,name):
		self.name = name
	
	
########

class Constant(Num):
	def __init__(self,value):
		self.name = value
		self.value = value

########

class Operation:
	def __init__(self,name):
		self.name = name
		return

	def is_operation(self,op_name):
		if self.name == op_name:
			return True
		else:
			return False
	

class Function:
	def __init__(self):
		self.instr_list = []
		return
	
	def add_instruction_by_label(self,label,instr):
		assert(isinstance(label,int) and isinstance(instr,Instruction))
		self.instr_list.append(instr)
		return
	
	def set_input_variables(self,input_variables):
		self.input_variables = input_variables
		return
	
	def set_output_variables(self,output_variables):
		self.output_variables = output_variables
		return

	def execute(self,input_values):
		n = 0
		for var in self.input_variables:
			var.value = input_values[n]
			n = n+1
		self.program_counter = 1
		label = 0
		end_reached = False
		program_counter = 0
		while end_reached is False:
			if program_counter is (len(self.instr_list)+1):
				end_reached = True
			elif isinstance(self.instr_list[program_counter],ReturnInstruction) is True:
				end_reached = True
			elif isinstance(self.instr_list[program_counter],ExecutableInstruction) is True:
				self.instr_list[program_counter].execute()
				program_counter = program_counter + 1
			else:
				program_counter = self.instr_list[program_counter].get_next_instr()
		output_values = []
		for var in self.output_variables:
			output_values.append(var.value)
		return output_values

	def show(self):
		label = 0
		for instr in self.instr_list:
			instr.set_label(label)
			label += 1
		for instr in self.instr_list:
			instr.show()
		return
	
	def print_variables(self):
		for var in self.input_variables:
			print var.name,' ',var.value
		for var in self.output_variables:
			print var.name,' ',var.value
	
	def add_summary(self,summary):
		assert(isinstance(summary,str))
		self.summary = summary
		return
