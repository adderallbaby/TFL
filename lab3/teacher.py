import sys

import nltk
from nltk.grammar import CFG
from nltk.parse.generate import generate

import angluin
import compatibility


def membership_query(word):
    word = list(word)
    f = open("grammar.txt", "r")
    grammar = CFG.fromstring(f.read())

    parser = nltk.EarleyChartParser(grammar)
    counter = 0
    for _ in parser.parse(word):
        counter += 1
        break
    f.close()
    return counter


def equivalence_query(transitions, endstates, initial, states, alphabet):
    f = open("grammar.txt", "r")
    grammar = CFG.fromstring(f.read())
    f.close()
    words = list(generate(grammar, n=20, depth=10))
    counter = 0
    for i in range(len(words)):
        cur = ''
        alph = []
        counter += 1
        for j in range(len(words[i])):
            cur += words[i][j]

            if words[i][j] not in alph:
                alph.append(words[i][j])
        if compatibility.satisfies(cur, transitions, endstates, initial) == 0 and set(alph) == set(alphabet):
            return 0, cur
    return 1, 'equivalent'


def main(alphabet, initial_regex):
    f = open("initial_regex.txt", "w")
    f.write(initial_regex)
    f.close()
    return angluin.main(alphabet)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
