import backend_elim
import teacher


answer = ''
E = []
SA = {}
S = {}
A = []
c = 0


class RegularExp:
    pass


def main(alphabet):
    global E, SA, S, A
    S = {}
    A = []
    for i in alphabet:
        A.append(i)
    E = ['']
    SA = {}
    S[''] = {'': teacher.membership_query('')}
    for a in A:
        SA[a] = {'': teacher.membership_query(a)}
    answer2 = learning(S, SA, A)
    return answer2


def closed(S, SA):
    for key, row in SA.items():
        if row not in S.values():
            return False, key, row
    return True, '', ''


def equivalence(A, S, SA, char_1, char_2):
    table = {**SA, **S}
    for a in A:
        if table[char_1 + a] != table[char_2 + a]:
            for key1, val1 in table[char_1 + a].items():
                for key2, val2 in table[char_2 + a].items():
                    if val1 != val2 and key1 == key2:
                        return False, a + key2
    return True, ''


def consistent(S, SA, A):
    for char_1 in S:
        for char_2 in S:
            if S[char_1] == S[char_2]:
                equ = equivalence(A, S, SA, char_1, char_2)
                if not equ[0]:
                    return False, equ[1]
    return True, ''


def rowtostring(row):
    s = ''
    for i in row.values():
        s += str(i)
    return s


def build_dfa(S, SA, A):
    initial_state = rowtostring(S[''])
    states = [initial_state]
    transitions = []
    final_states = []
    table = {**S, **SA}
    if S[''][''] == 1:
        final_states.append(initial_state)
    for key in S.keys():
        start = rowtostring(S[key])
        for a in A:
            k = key + a
            row = table[k]
            state = rowtostring(row)
            if state not in states:
                states.append(state)
            transition = {'source': start, 'dest': state, 'trigger': a}
            if transition not in transitions:
                transitions.append(transition)
        if S[key][''] == 1:
            if start not in final_states:
                final_states.append(start)
    return transitions, final_states, initial_state, states


def dfa_to_regex(transitions, states, initial_state, final_states):
    transitions = backend_elim.removeStates(transitions, states, initial_state, final_states)
    regular = ''
    for transition in transitions:
        if not (transition['trigger'] == ''):
            if '()' in transition['trigger']:
                regular += transition['trigger'].replace('()', '(ε)') + '|'
            else:
                regular += transition['trigger'] + '|'

    regular = regular[:-1]
    minRegex = regular
    return minRegex


def reduce_table(S, SA, char):
    for value in list(S.values()):
        value.pop(char)
    for value in list(SA.values()):
        value.pop(char)

    return S, SA


def learning(S, SA, A):
    global c, answer
    while not closed(S, SA)[0] or not consistent(S, SA, A)[0]:
        boo, char = consistent(S, SA, A)

        if not boo:
            if c < 100:
                c += 1
            table = {**S, **SA}
            E.append(char)
            for key, value in table.items():
                value[char] = teacher.membership_query(word=key + char)
            if c < 100:
                c += 1

        boo, key, row = closed(S, SA)
        if not boo:
            del SA[key]
            S = {**S, **{key: row}}
            for a in A:
                cur = {}
                k = key + a

                for e in E:
                    subcurr = {e: teacher.membership_query(k + e)}
                    cur = {**cur, **subcurr}
                SA = {**SA, **{k: cur}}
    
    transitions, final_states, initial_state, states = build_dfa(S, SA, A)

    boo, string = teacher.equivalence_query(transitions, final_states, initial_state,states , A)
    if not boo or string[1] == 'bigger':
        for i in range(1, len(string) + 1):
            t = string[0:i]
            if t in SA.keys():
                del SA[t]
            cur = {}

            for e in E:
                subcurr = {e: teacher.membership_query(t + e)}
                cur = {**cur, **subcurr}

            S = {**S, **{t: cur}}
            for a in A:
                cur = {}
                key = t + a
                for e in E:
                    subcurr = {e: teacher.membership_query(key + e)}
                    cur = {**cur, **subcurr}
                SA = {**SA, **{key: cur}}
        c += 1

        learning(S, SA, A)
    else:
        transitions, final_states, initial_state, states = build_dfa(S, SA, A)
        regular = dfa_to_regex(transitions.copy(), states.copy(), initial_state, final_states.copy())
        if len(regular) > 100:
            for e in E:
                if e == '':
                    continue
                transitions, final_states, initial_state, states = build_dfa(S, SA, A)
        answer = [transitions, states, initial_state, final_states]
    return answer
