import functions 
import FSMgenerator
import sys
import itertools
import backend_elim
from transitions import Machine
from transitions.extensions import GraphMachine
import deriv_generator
class Regex():
    pass
regex = Regex()


def main(alphabet, initial_regex):
    #alphabet ='' #input("Введите алфавит без пробелов и запятых (например, abcdef): ")
    #initial_regex =''#input("Введите regex: ")
    
    final_states, states,transitions, initial_regex = FSMgenerator.main(alphabet, initial_regex)
    #print(final_states)
    states = list(set(states))

    #for real in real_states:
    #    if real_states.count(real) > 1:
    #        real_states.remove(real)

    minRegex = 'a'*2555
    #print(real_states)
    #transitions.sort()
    #combinations = list(itertools.permutations(real_states, len(real_states)))
    #print(combinations)
    
    i = 0
        #        i+=1

    regex = Regex()

    machine = GraphMachine(model= regex, states=states, transitions=transitions, initial='INPUT',show_conditions=True)
    regex.get_graph().draw('prefinal.png', prog= 'dot')

    transitions = backend_elim.removeStates(transitions,states,initial_regex,final_states)
    regular = ''
    for transition in transitions:
        regular += transition['trigger'] + '|'
    regular = regular[:-1]
    #print(states)

    #print(regular)


    if '()' not in regular:
        regular = (deriv_generator.getBinaryTree(deriv_generator.getPostfix(deriv_generator.makeConcat(regular))))
    
        deriv_generator.postorder(regular)
        regular = deriv_generator.inorder(regular)
        #print(regular)
    
    #print(i)
    #if len(regular) < len(minRegex):
    minRegex = regular
    states = ['INPUT', 'OUTPUT']
    print(minRegex)
    regex = Regex()
    machine = GraphMachine(model= regex, states=states, transitions=transitions, initial='INPUT',show_conditions=True)
    regex.get_graph().draw('final.png', prog= 'dot')

    return minRegex



if __name__ == "__main__":
    minRegex = 'a'*255
    #for i in range(100):
    regular = main(sys.argv[1], sys.argv[2])
    #    if len(regular) < len(minRegex):
    #        minRegex = regular
    regex = Regex()
    #machine = GraphMachine(model= regex, states=states, transitions=transitions, initial='INPUT',show_conditions=True)
    #regex.get_graph().draw('final.png', prog= 'dot')

