import sys
sys.path.append('$newhome/epsilon/epsilon-1.0/epsilon_package/')
import cfg

## This class consists of functions which write to a verilog file
# Each instruction is considered a state and the transitions are defined in
# that way.
class VerilogWriter:
    ## The intializer, if takes in cfg and the verilog filename from the VerilogBackend class
    def __init__(self,name,cfg):
        print "Starting printing to verilog"
        ## The output file object
        self.out = open(name+".v",'w+')
        ## cfg object from the epsilon
        self.cfg = cfg
        ## No. of  bits required to represent states
        self.no_of_bits = 0
        ## Current state
        self.current_state = 0
        ## Denotes the state number of each basicblock, used to make the state determining easier.## Denotes the state number of each basicblock, used to make the state determining easier.
        self.bb_states = []

    ## The initial printing to file, prints module name and the ports in it.
    def print_init(self):
        print "Printing the interface"
        in_list = self.cfg.input_variable_list
        out_list = self.cfg.output_variable_list
        header = "module function(\n"
        self.out.write(header)
        for port in in_list:
            if port not in out_list:
                self.out.write(port.name+',\n')
        for port in out_list:
            self.out.write(port.name+',\n')
        self.out.write("clk ,\n")
        self.out.write("reset,\n")
        #now trace back a bit and close the braces after removing the last comma
        self.out.seek(-2,1)
        self.out.write(");\n")

    ## This function prints the input output port declarations and other
    # registers to the verilog file
    # BUG TODO : What to do if variable is both input and output.
    # BUG TODO : Scheduling and Allocation is not good!
    def print_registers(self):
        print "Printing the registers holding variables"
        inputs = self.cfg.input_variable_list
        outputs = self.cfg.output_variable_list
        for var in inputs:
            if var not in outputs:
                self.out.write("input [31:0] " + var.name + ";\n")
        self.out.write("input clk;\n")
        self.out.write("input reset;\n")
        for var in outputs:
            if var not in inputs:
                self.out.write("output [31:0] " + var.name + ";\n")
            else:
                self.out.write("inout [31:0] " + var.name + ";\n")

        register_variables = []
        for bb in self.cfg.basicblock_list: # Go through the cfg and give register to only those which are not in input or output and
            try:
                if isinstance(bb.condition_instr, cfg.Instruction):
                    for var in [bb.condition_instr.rhs_1,bb.condition_instr.rhs_2]:
                        if isinstance(var,cfg.Variable) and var not in register_variables:
                            register_variables.append(var)
                for ins in bb.instruction_list:
                    if isinstance(ins, cfg.ArithInstruction) or  isinstance(ins, cfg.EqInstruction):
                        if ins.lhs not in register_variables:
                            register_variables.append(ins.lhs)
            except:
                pass
        for var in register_variables:
            if var not in inputs and var not in outputs:
                self.out.write("reg [31:0] " + var.name + ";\n")
        no_of_states = self.find_no_of_states() #Each instruction is a state!
        print "There are",no_of_states,"states"
        bits_in_state = no_of_bits(no_of_states)
        self.no_of_bits = bits_in_state #
        self.out.write("reg ["+str(bits_in_state-1)+":0] state;\n\n")

    ## This function finds the number of states required going through all the
    # basic blocks in the cfg
    def find_no_of_states(self):
        n_states = 0
        self.bb_states = []
        for bb in self.cfg.basicblock_list:
            n_states = n_states + 1 #Each basic block has a conditional or jump instruction
            self.bb_states.append(n_states-1)
            print bb.identity, n_states-1
            n_states = n_states +bb.number_of_instructions
        return n_states

    ## The main function called which invokes the printing of all the basic
    # blocks in a loop
    def print_states(self):
        self.print_reset(0)
        print "Printing the state transitions"
        for bb in self.cfg.basicblock_list:
            print ""
            self.print_basic_block(bb)

    ## Print the reset block. Asynchronous reset: resets to state zero whenever
    # reset is LOW
    def print_reset(self,state):
        self.out.write("\t//Reset to state zero when reset is made LOW\n")
        self.out.write("\talways@(*) begin\n")
        self.print_if("reset","==","0")
        self.print_state_change(0)
        self.out.write("\t\tend\n")
        self.out.write("\tend\n\n")

    ## prints a basic block in a always @ () block in verilog
    # It loops though all instructions and invokes the printing of them
    def print_basic_block(self,bb):
        self.out.write("\t// Corresponding code for BasicBlock "+str(bb.identity)+"\n")
        self.out.write("\talways@ (negedge clk) begin\n")
        rel_state = 1
        for instr in bb.instruction_list:
            self.current_state = self.bb_states[bb.identity] + rel_state
            self.print_if("state","==",tobinary(self.current_state, self.no_of_bits))
            #State transitions go here.
            self.print_instruction(instr,bb)
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

    ## Prints the  arithmetic instruction with lhs op and rhs
    def print_instruction(self, instr, bb):
        if isinstance(instr, cfg.ArithInstruction):
            self.print_arith(instr.lhs.name,instr.rhs_1.name,instr.op.name,instr.rhs_2.name)
        elif isinstance(instr, cfg.EqInstruction):
            self.print_eq(instr.lhs.name,instr.rhs.name)
        print bb.number_of_instructions, bb.number_of_children
        try:
            print bb.condition,bb.condition_instr,"Conditional ins"
        except:
            pass
        for ins in bb.instruction_list:
            print ins

    ## Formatted arithmetic instruction printing to file
    def print_arith(self,var,lhs,op,rhs):
        self.out.write("\t\t\t"+str(var)+" <= "+str(lhs)+" "+str(op)+" "+str(rhs)+";\n")

    def print_eq(self,lhs,rhs):
        self.out.write("\t\t\t"+str(lhs)+" <= "+str(rhs)+";\n")

    ## Prints a conditional jump instruction uses several methods
    def print_condition(self,bb,condition):
        print "Printing condition :P"
        if condition:
            self.print_if(condition.rhs_1.name,condition.op.name,condition.rhs_2.name)
        else:
            self.print_if(bb.condition.name,"==",1)
        self.print_state_change(self.next_state(bb.child_true))
        self.out.write("\t\tend else begin\n")
        self.print_state_change(self.next_state(bb.child_false))
        self.out.write("\t\tend\n")

    ## Gives the next state number given the next basicblock to jump to
    def next_state(self,next_bb):
        if next_bb.number_of_instructions:
            next_state = self.bb_states[next_bb.identity]+1
        else:
            next_state = self.bb_states[next_bb.identity]
        return next_state

    ## Prints the state change verilog code to a given state
    def print_state_change(self,state):
        self.out.write("\t\t\tstate <= "+tobinary(state,self.no_of_bits)+";\n")

    ## Prints a if statement given the lhs op and rhs
    def print_if(self,lhs,op,rhs):
        self.out.write("\t\tif ("+str(lhs)+" "+str(op)+" "+ str(rhs) + ") begin\n")

    ## When finished, prints a endmodule
    def print_final(self):
        self.out.write("endmodule\n")
        print "Finished writing module"
        self.out.close()

    def print_testbench(self):
        print "Printing testbench"

## Other function to find no_of_bits required for the given no_of_states
def no_of_bits(states):
    n = states
    nbits=0
    while n>0:
        n=n/2
        nbits=nbits+1
    return nbits

## Changes a state to binary string of nbits bits
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










