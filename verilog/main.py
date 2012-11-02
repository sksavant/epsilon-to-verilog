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

class VerilogBackend(epsilon.Backend):
    def run(self):
        print self.parent
        temp_cfg = self.parent.the_cfg.root
        for x in temp_cfg.basicblock_list:
            print x
        print 'verilog backend running'
        return



vb = VerilogBackend(the_epsilon)
the_epsilon.register_backend(vb)
the_epsilon.run_backend()


the_epsilon.dump_ast()
the_epsilon.dump_cfg()
the_epsilon.dump_sim_assembly()
the_epsilon.run_simulator()
