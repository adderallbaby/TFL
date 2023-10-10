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
    #print('ε'.isalpha()) 
    final_states, states,transitions, initial_regex = FSMgenerator.main(alphabet, initial_regex)
    #print(final_states)
    states = list(set(states))
    #print(states)
    met = {}
    number = 0 
    for i in states:
        if not i in met.keys():
            met[i] = number 
            number+=1 
    matrixDlyaPashi = []
    #print(len(states))
    for i in range(len(states)):
        matrixDlyaPashi.append([0]*len(states))
    #print(met)
    for i in transitions:
        if not i['source'] in final_states:
            src = i['source']
            dest = i['dest']

            #print(src, met[src])
            #print(dest, met[dest])
            matrixDlyaPashi[met[src]][met[dest]] =  i['trigger']

    #print(matrixDlyaPashi)
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
                
    machine = GraphMachine(model= regex, states=states, transitions=transitions, initial=initial_regex,show_conditions=True)
    regex.get_graph().draw('prefinal.png', prog= 'dot')

    transitions = backend_elim.removeStates(transitions,states,initial_regex,final_states)
    regular = ''
    #print(transitions)
    for transition in transitions:
        #print(transition['trigger'])

        #if '()' not in transition['trigger']:
        if not ( transition['trigger'] == ''):

            #print(regular, "not")
            if '()' in transition['trigger']:
                #print(regular, 'reg')
                regular += transition['trigger'].replace('()', '(ε)') + '|'
                #print(regular, 'reg')

            #print(regular, 'yes)
            else:
                regular += transition['trigger'] + '|'

    regular = regular[:-1]
    #print(states)

    #print(regular)


    if '()' not in regular:
        regular = (deriv_generator.getBinaryTree(deriv_generator.getPostfix(deriv_generator.makeConcat(regular))))
    
        deriv_generator.postorder(regular)
        #regular = deriv_generator.inorder(regular)
        regular = functions.prettyInorder(regular)
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

