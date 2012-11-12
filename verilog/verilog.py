class VerilogWriter:
    def __init__(self,name):
        print "Starting printing to verilog"
        self.out = open(name+".v",'w+')

    def print_init(self,in_list, out_list):
        print "Printing the interface"
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
    # BUG TODO : Scheduling is bad!
    def print_registers(self,cfg):
        print "Printing the registers holding variables"
        for var in cfg.input_variable_list:
            self.out.write("input [31:0] " + var.name + ";\n")
        for var in cfg.output_variable_list:
            self.out.write("output [31:0] " + var.name + ";\n")
        for var in cfg.variable_list:
            if (var not in cfg.input_variable_list) and (var not in cfg.output_variable_list):
                self.out.write("reg [31:0] " + var.name + ";\n")
        no_of_states = len(cfg.basicblock_list) #Each basicblock is a state!
        bits_in_state = no_of_bits(no_of_states)
        self.out.write("reg ["+str(bits_in_state-1)+":0] state;\n")

    def print_final(self):
        self.out.write("\nendmodule\n")
        print "Finished writing module"
        self.out.close()

def no_of_bits(states):
    n = states
    nbits=0
    while n>0:
        n=n/2
        nbits=nbits+1
    return nbits












