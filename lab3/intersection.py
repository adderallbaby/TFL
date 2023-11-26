def isin(arr, el):
    for a in arr:
        if a == el:
            return True
    return False


def rename(transitions, states, endstates, initial):
    states.sort()
    newstates = []
    newendstates = []
    counter = 0
    for i in range(len(states)):
        if initial == states[i]:
            initial = counter
        newstates.append(counter)
        for j in range(len(transitions)):
            if transitions[j].get('source') == states[i]:
                if isin(endstates, transitions[j].get('source')) and not isin(newendstates, counter):
                    newendstates.append(counter)
                transitions[j].update({'source': counter})

            if transitions[j].get('dest') == states[i]:
                if isin(endstates, transitions[j].get('dest')) and not isin(newendstates, counter):
                    newendstates.append(counter)
                transitions[j].update({'dest': counter})
        counter += 1
    return transitions, newstates, newendstates, initial


def intersect(initial1, states1, transitions1, endstates1, initial2, states2, transitions2, endstates2):
    initial3 = int(str(initial1) + str(initial2))
    states3 = []
    transitions3 = []
    endstates3 = []

    for i in range(len(states1)):
        for j in range(len(states2)):
            states3.append(int(str(states1[i]) + str(states2[j])))
            if isin(endstates1, states1[i]) and isin(endstates2, states2[j]):
                endstates3.append(int(str(states1[i]) + str(states2[j])))

    for i in range(len(states1)):
        for j in range(len(states2)):
            for p in range(len(transitions1)):
                if transitions1[p].get('source') == states1[i]:
                    for q in range(len(transitions2)):
                        if transitions2[q].get('source') == states2[j] and transitions1[p].get('trigger') == transitions2[q].get('trigger'):
                            transitions3.append({'trigger': transitions1[p].get('trigger'), 'source': (str(states1[i]) + str(states2[j])), 'dest': (str(transitions1[p].get('dest')) + str(transitions2[q].get('dest')))})
                            break

    transitions3, states3, endstates3, initial3 = rename(transitions3, states3, endstates3, initial3)

    return initial3, states3, transitions3, endstates3


def unification(initial1, states1, transitions1, endstates1, initial2, states2, transitions2, endstates2):
    initial3 = (str(initial1) + str(initial2))
    states3 = []
    transitions3 = []
    endstates3 = []

    for i in range(len(states1)):
        for j in range(len(states2)):
            states3.append(int(str(states1[i]) + str(states2[j])))
            if isin(endstates1, states1[i]) or isin(endstates2, states2[j]):
                endstates3.append((str(states1[i]) + str(states2[j])))

    for i in range(len(states1)):
        for j in range(len(states2)):
            for p in range(len(transitions1)):
                if transitions1[p].get('source') == states1[i]:
                    for q in range(len(transitions2)):
                        if transitions2[q].get('source') == states2[j] and transitions1[p].get('trigger') == transitions2[q].get('trigger'):
                            transitions3.append({'trigger': transitions1[p].get('trigger'), 'source': (str(states1[i]) + str(states2[j])), 'dest': (str(transitions1[p].get('dest')) + str(transitions2[q].get('dest')))})
                            break

    transitions3, states3, endstates3, initial3 = rename(transitions3, states3, endstates3, initial3)

    return initial3, states3, transitions3, endstates3


def negation(initial, states, transitions, endstates):
    newendstates = []
    for i in range(len(states)):
        if not isin(endstates, states[i]):
            newendstates.append(states[i])
    return initial, states, transitions, endstates
