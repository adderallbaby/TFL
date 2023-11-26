import exrex
import CFGTOCNF
import CNF2PREFIX
import angluin
import teacher
import CNF2REVERSE
import processCNF
import intersection


class Regex:
    pass


C = 4
maxStates = 8


def satisfies(word, transitions, endstates, initial):
    current = initial
    for char in word:
        flag = 0
        for t in transitions:
            if t['source'] == current and t['trigger'] == char:
                current = t['dest']
                flag = 1
                break
        if flag == 0:
            return 0

    return current in endstates


def complement(transitions, states, initial_state, final_states):
    new_final = []
    for i in states:
        if i not in final_states:
            new_final.append(i)
    return transitions, states, initial_state, new_final


def pump(w_s, flag):
    strings = []
    if flag == 'prefix':
        for i in range(C):
            strings.append('')
        for i in range(0, C):
            s = exrex.getone(w_s[0], limit=5) + w_s[1] * i + w_s[2] + (w_s[3] * i)
            strings[i] = s
    elif flag == 'suffix':
        for i in range(C):
            strings.append('')
        for i in range(0, C):
            s = w_s[0] * i + w_s[1] + w_s[2] * i + exrex.getone(w_s[3], limit=3)
            strings[i] = s
    elif flag == 'all':
        for i in range(C):
            s = [exrex.getone(w_s[0], limit=3), w_s[1] * i, w_s[2], w_s[3] * i, exrex.getone(w_s[4], limit=3)]
            strings.append(s)

    return strings


def main(w1, w2, w3, w4, w5):
    CNF = CFGTOCNF.main('input.txt')

    CNF = processCNF.main(CNF)

    prefix = CNF2PREFIX.main(CNF)

    for i in range(len(prefix)):
        if prefix[i].isalpha() and prefix[i].islower() and not prefix[i - 1] == "'":
            prefix = prefix.replace(prefix[i], f"'{prefix[i]}'")

    f = open('grammar.txt', 'w')
    f.write(prefix)
    f.close()
    alphabet = ''
    for i in w1:
        if i.isalpha() and i not in alphabet:
            alphabet += i

    w1_transitions, w1_states, w1_initial_state, w1_final_states = teacher.main(alphabet, w1)
    ang_w1 = angluin.dfa_to_regex(w1_transitions, w1_states, w1_initial_state, w1_final_states).replace('ε', '')
    # print(ang_w1, 'w1')
    w1s = []
    pumping = pump([ang_w1, w2, w3, w4], 'prefix')
    c = C
    for i in pumping:
        if teacher.membership_query(i) == 1:
            # print(i, 'word w1')
            w1s.append(i)
        else:
            # print(i, 'doesnt fit')
            c -= 1
    # print(f'correct {c} out of {C}')

    CNF = CFGTOCNF.main('input.txt')

    CNF = processCNF.main(CNF)
    CNF = processCNF.start_to_top(CNF)
    reverse = CNF2REVERSE.main(CNF)

    reverse = CNF2PREFIX.main(reverse)
    reverse = processCNF.main(reverse)

    Terminals = ''
    Variables = ''
    Productions = ''
    reverse_list = reverse.split('\n')
    for row in reverse_list:
        prod = row.split()
        for a in prod:
            flag = 0
            for char in a:
                if char.isalpha() and char.islower():
                    Terminals += a + " "
                    flag = 1
                    break
            if flag == 0:
                if not a == '->' and a not in Variables:
                    Variables += a + " "
        Productions += row + ';\n'

    CFGo = CFGTOCNF.main('input.txt')

    reverse = CNF2REVERSE.main(CFGo)
    prefix = CNF2PREFIX.main(reverse)
    c = processCNF.main(prefix)
    suffix = CNF2REVERSE.main(c)

    CFGo = CFGTOCNF.main('input.txt')
    reverse = CNF2REVERSE.main(CFGo)
    prefix = CNF2PREFIX.main(reverse)
    c = processCNF.main(prefix)
    reverse = CNF2REVERSE.main(c)
    file = open('input.txt', 'r').read()
    alph_to_insert = (file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", ""))

    prod_to_insert = reverse.replace('\n', ' ;\n')[:-2]
    Variables = ''
    for i in reverse.split('\n'):
        a = i.split('->')[0].strip()
        if a not in Variables:
            Variables += a + ' '

    anti_w1_grammar = f'''Terminals:\n{alph_to_insert}\nVariables:\n{Variables[:-1]}\nProductions:\n{prod_to_insert}'''
    f = open('anti.txt', 'w')
    f.write(anti_w1_grammar)
    f.close()
    CFG_anti = CFGTOCNF.main('anti.txt')
    infix = processCNF.start_to_top(CFG_anti)
    for i in range(len(suffix)):
        if suffix[i].isalpha() and suffix[i].islower() and not suffix[i - 1] == "'":
            suffix = suffix.replace(suffix[i], f"'{suffix[i]}'")
    f = open('grammar.txt', 'w')
    f.write(suffix)
    f.close()

    alphabet = ''
    for i in w5:
        if i.isalpha() and i not in alphabet:
            alphabet += i
    w5_transitions, w5_states, w5_initial_state, w5_final_states = teacher.main(alphabet, w5)
    ang_w5 = angluin.dfa_to_regex(w5_transitions, w5_states, w5_initial_state, w5_final_states).replace('ε', '')
    # print(ang_w5, 'w5')

    pumping = pump([w2, w3, w4, ang_w5], 'suffix')
    w5s = []
    c = C

    for i in pumping:
        if teacher.membership_query(i) == 1:
            # print(i, 'word w5')

            w5s.append(i)
        else:
            # print(i, 'doesnt fit suffix')
            c -= 1
    # print(f'correct {c} out of {C}')
    pumping = pump([ang_w1, w2, w3, w4, ang_w5], 'all')
    CNF = CFGTOCNF.main('input.txt')
    for i in range(len(CNF)):
        if CNF[i].isalpha() and CNF[i].islower() and not CNF[i - 1] == "'":
            CNF = CNF.replace(CNF[i], f"'{CNF[i]}'")
    c = C
    CNF = processCNF.start_to_top(CNF)
    f = open('grammar.txt', 'w')
    f.write(CNF)
    f.close()
    counter_1 = []
    counter_5 = []
    for j in pumping:
        i = ''.join(j)
        if teacher.membership_query(i) == 1:
            print(i, 'word all')

            w5s.append(i)
        else:
            print(i, 'doesnt fit all')

            counter_1.append(j[0])
            counter_5.append(j[-1])
            c -= 1
    # print(f'correct {c} out of {C}')
    for i in range(len(infix)):
        if infix[i].isalpha() and infix[i].islower() and not infix[i - 1] == "'":
            infix = infix.replace(infix[i], f"'{infix[i]}'")
    f = open('grammar.txt', 'w')
    f.write(infix)

    f.close()
    alphabet = ''
    for i in w3:
        if i.isalpha() and i not in alphabet:
            alphabet += i
    w3_transitions, w3_states, w3_initial_state, w3_final_states = teacher.main(alphabet, w3)
    ang_w3 = angluin.dfa_to_regex(w3_transitions, w3_states, w3_initial_state, w3_final_states).replace('ε', '')
    # print(ang_w3, 'w3')

    alph_to_insert = (file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", ""))
    prod_to_insert = 'S -> '
    for i in counter_1:
        cur = ' '
        for j in i:
            cur += j + " "
        prod_to_insert += cur + '|'

    prod_to_insert = prod_to_insert[:-1]
    if not prod_to_insert.split('->')[1].strip() == "":

        anti_w1_grammar = f'''Terminals:\n{alph_to_insert}\nVariables:\nS\nProductions:\n{prod_to_insert}'''
        f = open('anti.txt', 'w')
        f.write(anti_w1_grammar)
        # print(anti_w1_grammar, 'anti')
        f.close()
        CFG_anti = CFGTOCNF.main('anti.txt')
        for i in range(len(CFG_anti)):
            if CFG_anti[i].isalpha() and CFG_anti[i].islower() and not CFG_anti[i - 1] == "'":
                CFG_anti = CFG_anti.replace(CFG_anti[i], f"'{CFG_anti[i]}'")
        f = open('grammar.txt', 'w')
        f.write(CFG_anti)
        f.close()
        a = ''
        for i in counter_1:
            for j in i:
                if j not in a:
                    a += j

        a_transitions, a_states, a_initial_state, a_final_states = teacher.main(a, prod_to_insert[5:])
        angluin.dfa_to_regex(a_transitions, a_states, a_initial_state, a_final_states).replace('ε', '')
        a_transitions, a_states, a_initial_state, a_final_states = complement(a_transitions, a_states, a_initial_state,
                                                                              a_final_states)

        a_initial_state, a_states, a_transitions, a_final_states = intersection.intersect(a_initial_state, a_states,
                                                                                          a_transitions, a_final_states,
                                                                                          w1_initial_state, w1_states,
                                                                                          w1_transitions,
                                                                                          w1_final_states)

        intersect_w1 = angluin.dfa_to_regex(a_transitions, a_states, a_initial_state, a_final_states).replace('ε', '')
        # print(intersect_w1, 'intersetion for w1')

    # else:
    #     print('empty complement', w1)

    alph_to_insert = (file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", ""))
    prod_to_insert = 'S -> '
    for i in counter_5:
        cur = ' '
        for j in i:
            cur += j + " "
        prod_to_insert += cur + '|'

    prod_to_insert = prod_to_insert[:-1]

    if not prod_to_insert.split('->')[1].strip() == "":
        anti_w5_grammar = f'''Terminals:\n{alph_to_insert}\nVariables:\nS\nProductions:\n{prod_to_insert}'''
        f = open('anti.txt', 'w')
        f.write(anti_w5_grammar)
        f.close()
        CFG_anti = CFGTOCNF.main('anti.txt')
        for i in range(len(CFG_anti)):
            if CFG_anti[i].isalpha() and CFG_anti[i].islower() and not CFG_anti[i - 1] == "'":
                CFG_anti = CFG_anti.replace(CFG_anti[i], f"'{CFG_anti[i]}'")
        f = open('grammar.txt', 'w')
        f.write(CFG_anti)
        f.close()
        a = ''
        for i in counter_5:
            for j in i:
                if j not in a:
                    a += j

        a_transitions, a_states, a_initial_state, a_final_states = teacher.main(a, prod_to_insert[5:])
        a_transitions, a_states, a_initial_state, a_final_states = complement(a_transitions, a_states, a_initial_state,
                                                                              a_final_states)
        a_initial_state, a_states, a_transitions, a_final_states = intersection.intersect(a_initial_state, a_states,
                                                                                          a_transitions, a_final_states,
                                                                                          w5_initial_state, w5_states,
                                                                                          w5_transitions,
                                                                                          w5_final_states)
        intersect_w5 = angluin.dfa_to_regex(a_transitions, a_states, a_initial_state, a_final_states).replace('ε', '')
    #     print(intersect_w5, 'intersetion for w5')
    # else:
    #     print('empty complement', w5)


if __name__ == '__main__':
    v1 = input('w1: ')
    v2 = input('w2: ')
    v3 = input('w3: ')
    v4 = input('w4: ')
    v5 = input('w5: ')
    main(v1, v2, v3, v4, v5)
