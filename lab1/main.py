
# This is a sample Python script.
import os
import subprocess

a_iterator = 0
b_iterator = 0
left_as = []
right_as = []
left_bs = []
right_bs = []

fnames = {}
# -------------------------
import sys


def formSMT2(ineqs):
    header = '(set-logic QF_NIA)\n'
    f = open('lab1.smt2', 'w')
    f.write(header)
    for val in fnames.values():
        f.write(f'(declare-fun {val[0]} () Int)\n')
        f.write(f'(declare-fun {val[1]} () Int)\n')
    for i in ineqs:
        f.write(f'(assert {i})\n')

    f.write('(check-sat)\n')
    f.write('(get-model)\n')
    f.write('(exit)')
    f.close()

def input():
    lefts = []
    rights = []
    for line in sys.stdin:
        if len(line) == 1:
            return lefts, rights
        lefts.append(line.split("->")[0].strip())
        rights.append(line.split("->")[1].strip())


def splitOnSameLvl(line, separator):
    t = []
    level = 1
    prev = 0
    for i in range(len(line)):
        char = line[i]
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        elif char == separator and level == 1:
            t.append(line[prev:i].strip())
            prev = i + 1
    t.append(line[prev:].strip())
    return t


def generateLinear(x, flag, fname):
    global left_as, right_as, left_bs, right_bs
    a = []
    global a_iterator, b_iterator
    linear = "(+ "
    if not fname in fnames.keys():
        for i in x:
            linear += f'(* a{a_iterator} {i}) '
            a.append(f'a{a_iterator}')

            a_iterator += 1
        linear += f"b{b_iterator})"
        a.append(f"b{b_iterator}")
        fnames[fname] = a

        b_iterator += 1
    else:
        coefs = fnames[fname]
        counter = 0
        for i in x:
            linear += f'(* {coefs[counter]} {i}) '
            counter += 1
        linear += f"{coefs[counter]})"

    return linear


def generateSingle(args, flag, fname):
    linear = generateLinear(args, flag, fname)
    for arg in args:
        if "(" in arg:
            func = arg[:arg.find('(')]

            cur = generateSingle(tuple(splitOnSameLvl(
                arg[arg.find('(') + 1:-1], ",")), flag, func)
            linear = linear.replace(arg, cur)
        else:
            return linear
    return linear


def generate(functions, flag):
    formed = []
    for function in functions:
        left = function.find("(") + 1
        right = function.rfind(")")
        f = function[:left - 1]
        x = generateSingle(tuple(splitOnSameLvl(function[left:right], ",")), flag, f)
        formed.append(x)
    return formed


def generateFirstInequality(left, right):
    left_side = "(* "
    left_funcs = left[:left.find('x')].split('(')[:-1]
    for func in left_funcs:
        left_side += fnames[func][0] + " "
    left_side += ")"
    right_side = "(* "

    right_funcs = right[:right.find('x')].split('(')[:-1]
    for func in right_funcs:
        right_side += fnames[func][0] + " "
    right_side += ")"

    return "(>= " + f'{left_side}' + " " + f'{right_side})'


def getall(idx, s, gl, funcs, a):
    if not idx == len(funcs) - 1:
        getall(idx + 1, s + a[funcs[idx]][0] + " ", gl, funcs, a)

    gl.append(s + a[funcs[idx]][1] + ")")
    return gl


def generateSecondInequality(left, right):
    left_side = "(+ "
    right_side = "(+ "
    l_right = left.find(')')
    funcs = left[:l_right].split('(')[:-1]
    left_elements = getall(0, "(* ", [], funcs, fnames)
    r_right = right.find(')')
    funcs = right[:r_right].split('(')[:-1]
    right_elements = getall(0, "(* ", [], funcs, fnames)
    for i in left_elements:
        s = i[1:-1]
        if len(s.split(" ")) == 2:
            i = s.split(' ')[1]
        left_side += i + " "
    left_side += ')'
    for i in right_elements:
        s = i[1:-1]
        if len(s.split(" ")) == 2:
            i = s.split(' ')[1]
        right_side += i + " "
    right_side += ')'
    return "(>= " + f'{left_side}' + " " + f'{right_side})'


def generateThirdInequality(left, right, second, first):
    second.replace("=", "")
    first.replace("=", "")
    return f'(or {first} {second})'


def generateFourthInequlaity(left, right, fnames):
    visited = []
    l_right = left.find(')')
    funcs = left[:l_right].split('(')[:-1]
    inequality = "(and "
    for func in funcs:
        if func not in visited:
            visited.append(func)
            inequality += f'(>= {fnames[func][0]}  1) '
            inequality += f'(>= {fnames[func][1]}  0) '
    r_right = right.find(')')
    funcs = right[:r_right].split('(')[:-1]
    for func in funcs:
        if func not in visited:
            visited.append(func)
            inequality += f'(>= {fnames[func][0]}  1) '
            inequality += f'(>= {fnames[func][1]} 0) '
    return inequality[:-1] + ")"


def generateFifthInequality(left, right, fnames):
    l_right = left.find(')')
    funcs = left[:l_right].split('(')[:-1]
    visited = []
    s = "(and "
    for func in funcs:
        if func not in visited:
            cur = f'(or (> {fnames[func][0]}  1) (> {fnames[func][1]}  0)) '
            s += cur
            visited.append(func)
    r_right = right.find(')')
    funcs = right[:r_right].split('(')[:-1]
    for func in funcs:
        if func not in visited:
            cur = f'(or ( > {fnames[func][0]}  1) (> {fnames[func][1]}  0)) '
            s += cur
            visited.append(func)
    return s + ")"


def main():
    print('Пример ввода:\nf(g(x)) -> g(f(x))\nf(h(x)) ->h(f(x))\n\nКак только на ввод поступает пустая строка, ввод считается завершенным')
    lefts, rights = input()
    ls = []
    # os.exec('z3 -h')
    l = generate(lefts, "left")
    r = generate(rights, "right")

    print(l[0])
    print(r[0])
    ineqs = []
    for i in range(len(rights)):
        ineqs.append(generateFirstInequality(lefts[i], rights[i]))
        ineqs.append(generateSecondInequality(lefts[i], rights[i]))
        ineqs.append(generateThirdInequality(lefts[i], rights[i], generateFirstInequality(lefts[i], rights[i]),
                                    generateSecondInequality(lefts[i], rights[i])))
        ineqs.append(generateFourthInequlaity(lefts[i], rights[i], fnames))
        ineqs.append(generateFifthInequality(lefts[i], rights[i], fnames))

    formSMT2(ineqs)
    print(fnames)


if __name__ == '__main__':
    main()

