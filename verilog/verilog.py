class VerilogWriter:
    def __init__(self,name,cfg):
        print "Starting printing to verilog"
        self.out = open(name+".v",'w+')
        self.cfg = cfg

    def print_init(self):
        print "Printing the interface"
        in_list = self.cfg.input_variable_list
        out_list = self.cfg.output_variable_list
        header = "module function(\n"
        self.out.write(header)
        for port in in_list:
            self.out.write(port.name+',\n')
        for port in out_list:
            self.out.write(port.name+',\n')
        self.out.write("clk ,\n")
        #now trace back a bit and close the braces after removing the last comma
        self.out.seek(-2,1)
        self.out.write(");\n")

    # BUG TODO : What to do if variable is both input and output.
    # BUG TODO : Scheduling and Allocation is not good!
    def print_registers(self):
        print "Printing the registers holding variables"
        inputs = self.cfg.input_variable_list
        outputs = self.cfg.output_variable_list
        variables = self.cfg.variable_list
        for var in inputs:
            self.out.write("input [31:0] " + var.name + ";\n")
        for var in outputs:
            self.out.write("output [31:0] " + var.name + ";\n")
        for var in variables:
            if var not in inputs and var not in outputs:
                self.out.write("reg [31:0] " + var.name + ";\n")
        no_of_states = self.find_no_of_states() #Each instruction is a state!
        print "There are",no_of_states,"states"
        bits_in_state = no_of_bits(no_of_states)
        self.no_of_bits = bits_in_state
        self.out.write("reg ["+str(bits_in_state-1)+":0] state;\n\n")

    def find_no_of_states(self):
        n_states = 0
        self.bb_states = []
        for bb in self.cfg.basicblock_list:
            n_states = n_states + 1 #Each basic block has a conditional or jump instruction
            self.bb_states.append(n_states-1)
            print bb.identity, n_states-1
            n_states = n_states +bb.number_of_instructions
        return n_states

    def print_states(self):
        print "Printing the state transitions"
        for bb in self.cfg.basicblock_list:
            print ""
            self.print_basic_block(bb)

    def print_basic_block(self,bb):
        self.out.write("\t// Corresponding code for BasicBlock "+str(bb.identity)+"\n")
        self.out.write("\talways@ (negedge clk) begin\n")
        rel_state = 1
        for instr in bb.instruction_list:
            self.current_state = self.bb_states[bb.identity] + rel_state
            self.print_if("state","==",tobinary(self.current_state, self.no_of_bits))
            #State transitions go here.
            self.print_state_transitions(instr,bb)
            self.out.write("\t\tend\n")
            rel_state = rel_state + 1
        #After all the instructions in instruction list state the jump or conditional statement
        self.print_if("state","==",tobinary(self.bb_states[bb.identity],self.no_of_bits))
        if bb.number_of_children == 1:
            self.print_state_change(self.bb_states[bb.child.identity])
        elif bb.number_of_children == 2:
            #2 children \implies comparision?
            self.print_condition(bb, bb.condition_instr)
        self.out.write("\t\tend\n")
        #debugging etc ... ignore : TODO to clean up
        self.out.write("\tend\n\n")

    def print_state_transitions(self, instr, bb):
        self.print_arith(instr.lhs.name,instr.rhs_1.name,instr.op.name,instr.rhs_2.name)
        print bb.number_of_instructions, bb.number_of_children
        try:
            print bb.condition,bb.condition_instr,"Conditional ins"
        except:
            pass
        for ins in bb.instruction_list:
            print ins

    def print_arith(self,var,lhs,op,rhs):
        self.out.write("\t\t\t"+var+" <= "+lhs+" "+op+" "+rhs+";\n")

    def print_condition(self,bb,condition):
        print "Printing condition :P"
        self.print_if(condition.rhs_1.name,condition.op.name,condition.rhs_2.name)
        self.print_state_change(self.next_state(bb.child_true))
        self.out.write("\t\telse begin\n")
        self.print_state_change(self.next_state(bb.child_false))
        self.out.write("\t\tend\n")

    def next_state(self,next_bb):
        if next_bb.number_of_instructions:
            next_state = self.bb_states[next_bb.identity]
        else:
            next_state = self.bb_states[next_bb.identity]+1
        return next_state

    def print_state_change(self,state):
        self.out.write("\t\t\tstate <= "+tobinary(state,self.no_of_bits)+";\n")

    def print_if(self,lhs,op,rhs):
        self.out.write("\t\tif ("+str(lhs)+" "+str(op)+" "+ str(rhs) + ") begin\n")

    def print_final(self):
        self.out.write("endmodule\n")
        print "Finished writing module"
        self.out.close()

def no_of_bits(states):
    n = states
    nbits=0
    while n>0:
        n=n/2
        nbits=nbits+1
    return nbits

def tobinary(state, nbits):
    n = state
    bit_string = ""
    while(n>0):
        bit = n%2
        n = n/2
        bit_string = bit_string + str(bit)
    bit_string=bit_string[::-1]
    assert(len(bit_string) <= nbits)
    if len(bit_string)<nbits:
        bit_string="0"*(nbits-len(bit_string))+bit_string
    return str(nbits) + "\'b" + bit_string










