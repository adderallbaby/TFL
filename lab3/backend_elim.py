def addEpsilons(transitions, initial_regex, final_states):
    for final in final_states:
        if final == "FINAL":
            continue
        transitions.append({'source': final, 'dest': 'FINAL', 'trigger': ''})
    transitions.append({'dest': initial_regex, 'source': 'INPUT', 'trigger': ''})


def loopsToString(transitions):
    if len(transitions) > 1:
        string = '('
        for transition in transitions:
            string += transition['trigger'] + '|'
        string = string[:-1] + ')*'

        return string
    elif len(transitions) == 1:
        return transitions[0]['trigger'] + '*'
    elif len(transitions) == 0:
        return ''


def eliminateStates(transitions, states):
    for state in states:
        newArr = []
        ins = []
        outs = []
        loops = []
        for transition in transitions:
            if transition['dest'] == state and not transition['source'] == state:
                ins.append(transition)
            elif transition['source'] == state and not transition['dest'] == state:
                outs.append(transition)
            elif transition['dest'] == state and transition['source'] == state:
                loops.append(transition)
        augment = loopsToString(loops)
        for i in ins:
            for o in outs:
                transitions.append({'source': i['source'], 'dest': o['dest'],
                                    'trigger': '(' + i['trigger'] + augment + o['trigger'] + ')'})
        for transition in transitions:
            if transition not in ins and transition not in outs and transition not in loops:
                newArr.append(transition)
        transitions = newArr
    return transitions


def removeStates(transitions, states, initial_regex, final_states):
    addEpsilons(transitions, initial_regex, final_states)
    if initial_regex in final_states:
        states.remove(initial_regex)
        states.append(initial_regex)
    transitions = eliminateStates(transitions, states)
    return transitions
