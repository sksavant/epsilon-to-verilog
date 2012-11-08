import sys
from optparse import OptionParser
sys.path.append('$newhome/epsilon/epsilon-1.0/epsilon_package/')

import epsilon

parser = OptionParser("usage: %epsilon [options] filename",
            version="epsilon 1.0")
parser.add_option("-i","--input_file",action="store",dest="source_filename",
        default="source.epsilon", help="enter path of the source code ")

(options,args) = parser.parse_args()

the_epsilon = epsilon.Epsilon()
the_epsilon.run_frontend(options.source_filename)

#############################################################################
#############################################################################
##VerilogBackend class is an example verilog backend which contains         #
# the code to write which will write to a verilog file given the            #
# cfg (control flow graph). The class should contain a "run(self)" method   #
####                                                                    #####
# Following is some explanation of the structure of the epsilon, cfg        #
# and how to go about writing the verilog backend :                         #
# 'parent' of this class gives the epsilon.Epsilon object (the main object) #
# epsilon.Epsilon consists of a epsilon.CFG object "the_cfg"                #
# the_cfg.root is a instance object of cfg.Function instance (~ temp_cfg)   #
# cfg.Function consists of lists of various things like :                   #
#  - basicblock_list                                                        #
#  - variable_list                                                          #
#  - input_variable_list                                                    #
#  - output_variable_list                                                   #
# 
#############################################################################
class VerilogBackend(epsilon.Backend):
    def run(self):
        print 'Verilog backend up and running'
        temp_cfg = self.parent.the_cfg.root
        self.print_info(temp_cfg)
        return
    
    def print_info(self,cfg):
        print 'Printing the info of the cfg...'
        #print self.parent
        #print self.parent.the_cfg
        #print temp_cfg
        _vl = cfg.variable_list
        _ivl = cfg.input_variable_list
        _ovl = cfg.output_variable_list
        _bbl = cfg.basicblock_list
        print "There are",len(_vl),"variables in total, namely: "
        for _v in _vl:
            print _v.name
        print "Of them,",len(_ivl),"is/are input variables, which are: "
        for _v in _ivl:
            print _v.name
        print "And",len(_ovl),"is/are output variables: "
        for _v in _ovl:
            print _v.name
        print ""
        print "There is/are",len(_bbl),"basicblocks"
        #for x in temp_cfg.basicblock_list:
        #    print x
        return
    
#############################################################################
## End of VerilogBackend Class                                              #
#############################################################################

vb = VerilogBackend(the_epsilon)
the_epsilon.register_backend(vb)
the_epsilon.run_backend()

#the_epsilon.dump_ast()
#the_epsilon.dump_cfg()
#the_epsilon.dump_sim_assembly()
the_epsilon.run_simulator()
