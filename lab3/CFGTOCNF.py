import helper
import sys

left, right = 0, 1

K, V, Productions = [], [], []
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "W", "X", "Y", "Z", "AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ", "KK", "LL", "MM", "NN", "OO", "PP", "QQ", "RR", "SS", "TT", "UU",
                "WW", "XX", "YY", "ZZ", "AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL", "MMM", "NNN", "OOO", "PPP", "QQQ", "RRR", "SSS", "TTT", "UUU",
                "WWW", "XXX", "YYY", "ZZZ"]


def isUnitary(rule, variables):
    if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
        return True
    return False


def isSimple(rule):
    if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
        return True
    return False


for nonTerminal in V:
    if nonTerminal in variablesJar:
        variablesJar.remove(nonTerminal)


def DEMIX(productions, variables, terminals):
    toRM = []

    for rulee in productions:
        inT = 0
        inV = 0
        rule = [rulee[0], ' '.join(rulee[1])]
        right = rule[1].split()
        char = ''
        for symbol in right:
            current = symbol.strip()
            if current in variables:
                inV = 1
            if current in terminals:
                inT = 1
                char = current

        if inT == 1 and inV == 1:
            for i in productions:
                if i[1] == [char]:
                    break

            for v in variablesJar:
                if v not in variables:
                    variables.append(v)
                    rule2 = (rule[0], rule[1].replace(char, v).split())
                    rule3 = (f'{v}', [f'{char}'])
                    productions.append(rule3)
                    productions.append(rule2)
                    toRM.append(rulee)
                    break

    for i in toRM:
        productions.remove(i)
    return productions


def START(productions, variables):
    variables.append('S')
    return [('S', [variables[0]])] + productions


def TERM(productions, variables):
    newProductions = []
    dictionary = helper.setupDict(productions, variables, terms=K)
    for production in productions:
        if isSimple(production):
            newProductions.append(production)
        else:
            for term in K:
                for index, value in enumerate(production[right]):
                    if term == value and term not in dictionary:
                        dictionary[term] = variablesJar.pop()
                        V.append(dictionary[term])
                        newProductions.append((dictionary[term], [term]))

                        production[right][index] = dictionary[term]
                    elif term == value:
                        production[right][index] = dictionary[term]
            newProductions.append((production[left], production[right]))
    return newProductions


def BIN(productions, variables):
    result = []
    for production in productions:
        k = len(production[right])
        if k <= 2:
            result.append(production)
        else:
            newVar = variablesJar.pop(0)
            variables.append(newVar + '1')
            result.append((production[left], [production[right][0]] + [newVar + '1']))
            for i in range(1, k - 2):
                var, var2 = newVar + str(i), newVar + str(i + 1)
                variables.append(var2)
                result.append((var, [production[right][i], var2]))
            result.append((newVar + str(k - 2), production[right][k - 2:k]))
    return result


def DEL(productions):
    newSet = []
    outlaws, productions = helper.seekAndDestroy(target='e', productions=productions)
    for outlaw in outlaws:
        for production in productions + [e for e in newSet if e not in productions]:
            if outlaw in production[right]:
                newSet = newSet + [e for e in helper.rewrite(outlaw, production) if e not in newSet]

    return newSet + ([productions[i] for i in range(len(productions))
                      if productions[i] not in newSet])


def unit_routine(rules, variables):
    unitaries, result = [], []
    for aRule in rules:
        if isUnitary(aRule, variables):
            unitaries.append((aRule[left], aRule[right][0]))
        else:
            result.append(aRule)
    for uni in unitaries:
        for rule in rules:
            if uni[right] == rule[left] and uni[left] != rule[left]:
                result.append((uni[left], rule[right]))

    return result


def UNIT(productions, variables):
    i = 0
    result = unit_routine(productions, variables)
    tmp = unit_routine(result, variables)
    while result != tmp and i < 1000:
        result = unit_routine(tmp, variables)
        tmp = unit_routine(result, variables)
        i += 1
    return result


def NORMALIZE(productions, variables):
    nums = []
    for i in range(1, 10):
        nums.append(str(i))
    for i in productions:
        s = i[0] + ' '.join(i[1])
        for n in nums:
            if n in s:
                for v in variablesJar:
                    if v not in variables:
                        pass

    return productions


def main(modelPath):
    K, V, Productions = helper.loadModel(modelPath)
    Productions = START(Productions, variables=V)
    Productions = TERM(Productions, variables=V)
    Productions = BIN(Productions, variables=V)
    Productions = DEL(Productions)
    Productions = UNIT(Productions, variables=V)
    Productions = DEMIX(Productions, V, K)
    A = helper.prettyForm(Productions).split('\n')
    A2 = []
    for line in A:
        if '|' in line:

            parts = line.split('|')
            for i in range(len(parts)):
                part = parts[i]
                if i == 0:
                    A2.append(f'{part}\n')
                else:
                    A2.append(f'{line[0]} ->{part}\n')
        else:
            A2.append(line + '\n')
    return ''.join(A2)


if __name__ == '__main__':
    main(sys.argv[1])
