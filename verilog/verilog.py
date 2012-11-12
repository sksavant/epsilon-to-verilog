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
        no_of_states = len(self.cfg.basicblock_list) #Each basicblock is a state!
        bits_in_state = no_of_bits(no_of_states)
        self.no_of_bits = bits_in_state
        self.out.write("reg ["+str(bits_in_state-1)+":0] state;\n\n")

    def print_states(self):
        print "Printing the state transitions"
        for bb in self.cfg.basicblock_list:
            self.print_basic_block(bb)

    def print_basic_block(self,bb):
        state = bb.identity
        self.out.write("\t// Corresponding code for BasicBlock "+str(state)+"\n")
        self.out.write("\talways@ (negedge clk) begin\n")

        self.out.write("\tend\n\n")
        self.print_if("state","==",tobinary(state,self.no_of_bits))

    def print_if(self,lhs,op,rhs):
        self.out.write("if ("+lhs+" "+op+" "+ rhs)

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










