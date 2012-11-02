# the ultimate module which would be the interface to the the end user
import eps_grammar
import ast
import cfg
import sim
import os

class Epsilon:
    def __init__(self):
        self.the_frontend = Frontend(self)
        self.the_simulator = Simulator(self)
        self.the_optimizer = Optimizer(self)
        self.the_backend = Backend(self)
        self.the_cfg = CFG(self)
        self.the_ast = AST(self)
        self.frontend_built = False #ast + cfg
        self.simulator_built = False
        self.backend_registered = False
        return

    def run_frontend(self,eps_filename):
        assert(isinstance(eps_filename,str))
        self.the_frontend.set_eps_filename(eps_filename)
        self.the_frontend.run()
        self.frontend_built = True
        return

    def run_simulator(self):
        if self.frontend_built is False:
            print 'please run frontend before running simulator'
        elif self.simulator_built is False:
            self.the_simulator.build_sim()
            self.the_simulator.run()
        else:
            self.the_simulator.run()
        return

    def run_optimization_passes(self,pass_names):
        for pass_name in pass_names:
            self.the_optimizer.add_pass_name(pass_name)
            self.the_optimizer.run_pass(pass_name)
        return

    def register_backend(self,the_backend):
        assert(isinstance(the_backend,Backend))
        self.the_backend = the_backend
        self.backend_registered = True
        return

    def run_backend(self):
        if self.frontend_built is False:
            print 'please run frontend before running backend'
        elif self.backend_registered is False:
            print 'no backend registered yet'
        else:
            self.the_backend.run()
        return

    def dump_ast(self):
        if self.frontend_built is False:
            print 'please run frontend before dumping ast'
        else:
            self.the_ast.show()
        return

    def dump_cfg(self):
        if self.frontend_built is False:
            print 'please run frontend before dumping cfg'
        else:
            self.the_cfg.show()

    def dump_sim_assembly(self):
        if self.frontend_built is False:
            print 'please run frontend before dumping assembly'
        elif self.simulator_built is False:
            self.the_simulator.build_sim()
            self.the_simulator.show()
        else:
            self.the_simulator.show()


############ Frontend ##############



class Frontend:
    def __init__(self,parent):
        self.parent = parent
        return

    def set_eps_filename(self,eps_filename):
        self.eps_filename = eps_filename
        return

    def run(self):
        #update the_ast and then update parent.the_cfg
        try:
            source_file = open(self.eps_filename,'r')
        except IOError:
            print 'error in opening file ', self.eps_filename
            quit()
        self.source = ""
        for line in source_file:
            self.source += line

        self.parent.the_ast.set_root(eps_grammar.get_ast(self.source))
        self.parent.the_cfg.set_root(self.parent.the_ast.get_cfg())

        return

############ Simulator ##############

class Simulator:
    def __init__(self,parent):
        assert(isinstance(parent,Epsilon))
        self.parent = parent
        self.running = False
        self.root = sim.Function()
        self.sim_var_list = []
        self.cfg_var_list = []
        self.sim_bb_label_list = []
        return

    def run(self):
        self.running = True
        while self.running is True:
            cmd = raw_input('eps $ ')
            self.handle_cmd(cmd)
        return

    def handle_cmd(self,cmd):
        if (cmd == 'exit'):
            self.running = False
        elif (cmd == ''):
            self.running = True
        elif (cmd == 'summary'):
            print ''
            print self.sim_func.summary
            print ''
        elif (cmd == 'help'):
            print ''
            print 'summary  : show summary of function as written in epsilon program'
            print 'exit     : exit simulator'
            print 'asm      : display intermediate code that is being simulated'
            print 'clear    : clear screen'
            print ''
        elif (cmd == 'clear'):
            os.system('clear')
        elif (cmd == 'asm'):
            print ''
            self.sim_func.show()
            print ''
        else:
            input_values_string = cmd.split(' ')
            input_values = []
            valid_input = True
            for value_string in input_values_string:
                try:
                    input_values.append(int(value_string))
                except:
                    valid_input = False
            if valid_input:
                if len(input_values) == len(self.sim_func.input_variables):
                    print self.sim_func.execute(input_values)
                else:
                    print 'expected ',len(self.sim_func.input_variables),' arguments'
            else:
                print 'please enter only integers as arguments'

    def build_sim(self):
        assert(isinstance(self.parent.the_cfg,CFG))
        cfg_func = self.parent.the_cfg.root
        self.sim_func = sim.Function()
        for cfg_var in cfg_func.variable_list:
            sim_var = sim.Variable(cfg_var.name)
            self.sim_var_list.append(sim_var)
            self.cfg_var_list.append(cfg_var)
        label = 0
        for cfg_bb in cfg_func.basicblock_list:
            self.sim_bb_label_list.append(label)
            for cfg_instr in cfg_bb.instruction_list:
                if isinstance(cfg_instr,cfg.ArithInstruction):
                    sim_instr = sim.ArithInstruction(self.sim_func)
                    sim_lhs = self.get_sim_numeric(cfg_instr.lhs)
                    sim_rhs_1 = self.get_sim_numeric(cfg_instr.rhs_1)
                    sim_rhs_2 = self.get_sim_numeric(cfg_instr.rhs_2)
                    sim_op = sim.Operation(cfg_instr.op.name)
                    sim_instr.update(sim_lhs,sim_rhs_1,sim_rhs_2,sim_op)
                elif isinstance(cfg_instr,cfg.CmpInstruction):
                    sim_instr = sim.CmpInstruction(self.sim_func)
                    sim_lhs = self.get_sim_numeric(cfg_instr.lhs)
                    sim_rhs_1 = self.get_sim_numeric(cfg_instr.rhs_1)
                    sim_rhs_2 = self.get_sim_numeric(cfg_instr.rhs_2)
                    sim_op = sim.Operation(cfg_instr.op.name)
                    sim_instr.update(sim_lhs,sim_rhs_1,sim_rhs_2,sim_op)
                elif isinstance(cfg_instr,cfg.EqInstruction):
                    sim_instr = sim.EqInstruction(self.sim_func)
                    sim_lhs = self.get_sim_numeric(cfg_instr.lhs)
                    sim_rhs = self.get_sim_numeric(cfg_instr.rhs)
                    sim_instr.update(sim_lhs,sim_rhs)
                self.sim_func.add_instruction_by_label(label,sim_instr)
                label +=1
            #at end of BB, add branch statements
            if cfg_bb.number_of_children is 1:
                sim_instr = sim.UncondnJumpInstruction(self.sim_func)
                self.sim_func.add_instruction_by_label(label,sim_instr)
            elif cfg_bb.number_of_children is 2:
                if isinstance(cfg_bb.condition_instr,cfg.CmpInstruction):
                    sim_instr = sim.CmpInstruction(self.sim_func)
                    sim_lhs = self.get_sim_numeric(cfg_bb.condition_instr.lhs)
                    sim_rhs_1 = self.get_sim_numeric(cfg_bb.condition_instr.rhs_1)
                    sim_rhs_2 = self.get_sim_numeric(cfg_bb.condition_instr.rhs_2)
                    sim_op = sim.Operation(cfg_bb.condition_instr.op.name)
                    sim_instr.update(sim_lhs,sim_rhs_1,sim_rhs_2,sim_op)
                    self.sim_func.add_instruction_by_label(label,sim_instr)
                    label+=1
                sim_instr = sim.CondnJumpInstruction(self.sim_func)
                sim_condn_var = self.get_sim_numeric(cfg_bb.condition)
                sim_instr.update(sim_condn_var,0,0)
                self.sim_func.add_instruction_by_label(label,sim_instr)
            else:
                sim_instr = sim.ReturnInstruction(self.sim_func)
                self.sim_func.add_instruction_by_label(label,sim_instr)
            label +=1

        k = 0
        for cfg_bb in cfg_func.basicblock_list:
            if cfg_bb.number_of_children is 1:
                this_label = self.sim_bb_label_list[k] + cfg_bb.number_of_instructions
                assert(isinstance(self.sim_func.instr_list[this_label],sim.UncondnJumpInstruction))
                next_label = self.sim_bb_label_list[cfg_bb.child.identity]
                self.sim_func.instr_list[this_label].next_instr_label = next_label
            elif cfg_bb.number_of_children is 2:
                this_label = self.sim_bb_label_list[k] + cfg_bb.number_of_instructions
                if isinstance(cfg_bb.condition_instr,cfg.CmpInstruction):
                    this_label += 1
                assert(isinstance(self.sim_func.instr_list[this_label],sim.CondnJumpInstruction))
                next_true_label = self.sim_bb_label_list[cfg_bb.child_true.identity]
                next_false_label = self.sim_bb_label_list[cfg_bb.child_false.identity]
                self.sim_func.instr_list[this_label].instr_true_label = next_true_label
                self.sim_func.instr_list[this_label].instr_false_label = next_false_label
            k+=1
        sim_input_variables = []
        for cfg_var in cfg_func.input_variable_list:
            sim_var = self.get_sim_numeric(cfg_var)
            sim_input_variables.append(sim_var)

        sim_output_variables = []
        for cfg_var in cfg_func.output_variable_list:
            sim_var = self.get_sim_numeric(cfg_var)
            sim_output_variables.append(sim_var)
        self.sim_func.set_input_variables(sim_input_variables)
        self.sim_func.set_output_variables(sim_output_variables)
        self.sim_func.add_summary(cfg_func.summary)
        assert(isinstance(self.root,sim.Function))
        return

    def get_sim_numeric(self,cfg_num):
        assert(isinstance(cfg_num,cfg.Numeric))
        if isinstance(cfg_num,cfg.Variable):
            k = 0
            for cv in self.cfg_var_list:
                if cv == cfg_num:
                    return self.sim_var_list[k]
                k = k+1
            return None
        else:
            return sim.Constant(cfg_num.value)

    def show(self):
        self.sim_func.show()

############ Optimizer ##############

class Optimizer:
    def __init__(self,parent):
        assert(isinstance(parent,Epsilon))
        self.parent = parent
        self.pass_names = []
        return

    def add_pass_name(self,pass_name):
        self.pass_names.append(pass_name)
        return

    def run_pass(self,pass_name):
        #run the pass on parent.the_cfg
        return


############ Backend ##############

class Backend:
    def __init__(self,parent):
        assert(isinstance(parent,Epsilon))
        self.parent = parent
        return

    def run(self):
        return

############ CFG ##############

class CFG:
    def __init__(self,parent):
        assert(isinstance(parent,Epsilon))
        self.parent = parent
        return

    def set_root (self,root_function):
        assert(isinstance(root_function,cfg.Function))
        self.root = root_function
        return

    def show (self):
        self.root.show()
        return

    def get_sim(self):
        return self.root.get_sim()


############ AST ##############
class AST:
    def __init__(self,parent):
        self.parent = parent
        return

    def set_root (self,root_function):
        assert(isinstance(root_function,ast.Function))
        self.root = root_function
        return

    def show (self):
        self.root.show()
        return

    def get_cfg(self):
        return self.root.get_cfg()
