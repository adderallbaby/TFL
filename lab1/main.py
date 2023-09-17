# This is a sample Python script.
import os
import subprocess

a_iterator = 0
b_iterator = 0
left_as = []
right_as = []
left_bs = []
right_bs = []
toDeclare = []
fnames = {}
E = [[1,0],
     [0,1]]
O = [[0,0], [0,0]]

# -------------------------
import sys

def matrixGreaterThan(A,B):
    ineqs = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            ineqs.append(f'(arcgg {A[i][j]} {B[i][j]})')
    return ineqs

def matrixGreaterOrEqualTo(A,B):
    ineqs = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            ineqs.append(f'(arcgg {A[i][j]} {B[i][j]})')
    return ineqs
def expandToMatrix(element, width):
    global toDeclare
    matrix = [[0] * width, [0] * width]
    if width == 2:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = element +f'{i}{j}'
                if element +f'{i}{j}' not in toDeclare:
                    toDeclare.append(element +f'{i}{j}')
        return matrix
    else:
        if element + '0' not in toDeclare:
            toDeclare.append(element + '0')
        if element + '1' not in toDeclare:
            toDeclare.append(element + '1')
        matrix[0][0] = element + '0'
        matrix[1][0] = element + '1'
        return matrix
def formSMT2(ineqs):
    global toDeclare
    header = '(set-logic QF_NIA)\n' \
             '(define-fun arcmax ((a Int) (b Int)) Int\n' \
    '(ite (>= a b)a b))\n' \
'(define-fun arcsum ((a Int) (b Int)) Int\n' \
    '(ite (and (> a -1)  (> b -1)) (+ a b) (ite (<= a -1) b a )))\n ' \
'(define-fun arcgg ((a Int) (b Int)) Bool\n' \
    '(ite (or (> a b) (and (<= a -1) (<= b -1))) true false))\n'
    f = open('lab1.smt2', 'w')
    f.write(header)
    visited= []
    for val in toDeclare:
        if val not in visited:
            f.write(f'(declare-fun {val} () Int)\n')
    for i in ineqs:
        f.write(f'(assert {i})\n')
    for i in toDeclare:
        if (i.startswith('a') and i.endswith('00')):
            f.write(f'(assert (> {i} -1))\n')
        if (i.startswith('b') and i.endswith('1')):
            f.write(f'(assert (or (> {i} -1) (and (= 0 {i[:-1]}0) (= 0 {i} ))))\n')

    f.write('(check-sat)\n')
    f.write('(get-model)\n')
    f.write('(exit)')
    f.close()


def arctic_mult_2x2(X,Y):
    result = [[0, 0],
              [0, 0]]
    result[0][0] = f'(arcmax (arcsum {X[0][0]} {Y[0][0]}) (arcsum {X[0][1]} {Y[1][0]}))'
    result[0][1] = f'(arcmax (arcsum {X[0][0]} {Y[0][1]}) (arcsum {X[0][1]} {Y[1][1]}))'
    result[1][0] = f'(arcmax (arcsum {X[1][0]} {Y[0][0]}) (arcsum {X[1][1]} {Y[1][0]}))'
    result[1][1] = f'(arcmax (arcsum {X[1][0]} {Y[0][1]}) (arcsum {X[1][1]} {Y[1][1]}))'
    return result

def arctic_mult_2x1(X,Y):
    result = [[0],[0]]

    result[0][0] = f'(arcmax (arcsum {X[0][0]} {Y[0][0]}) (arcsum {X[0][1]} {Y[1][0]}))'
    result[1][0] = f'(arcmax (arcsum {X[1][0]} {Y[0][0]}) (arcsum {X[1][1]} {Y[1][0]}))'
    return result
def arctic_mult(X,Y):
    if(len(Y[0]) == 1):
        return arctic_mult_2x1(X,Y)
    elif(len(Y[0]) == 2):
        return arctic_mult_2x2(X,Y)
def arctic_sum_1x1(X,Y):
    result = [[0],[0]]
    result[0][0] = f'(arcsum {X[0][0]} {Y[0][0]})'
    result[1][0] = f'(arcsum {X[1][0]} {Y[1][0]})'
    return result
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
    left_funcs = left[:left.find('x')].split('(')[:-1]
    prev = []
    for func in left_funcs:
        m = expandToMatrix(fnames[func][0],2)
        if prev == []:
            prev = m
        else:
            prev = arctic_mult_2x2(prev,m)
    r_prev = []
    right_funcs = right[:right.find('x')].split('(')[:-1]
    for func in right_funcs:
        m = expandToMatrix(fnames[func][0], 2)
        if r_prev == []:
            r_prev = m
        else:
            r_prev = arctic_mult_2x2(r_prev, m)
    ineq = '(and '
    for i in range(len(prev)):
        for j in range(len(prev[i])):
            ineq += f'(arcgg {prev[i][j]} {r_prev[i][j]}) '
    return ineq[:-1] + ')'


def getall(idx, s, gl, funcs, a):
    if not idx == len(funcs) - 1:
        getall(idx + 1, s + a[funcs[idx]][0] + " ", gl, funcs, a)

    gl.append(s + a[funcs[idx]][1] + ")")
    return gl


def generateSecondInequality(left, right):
    global a11, b1
    l_right = left.find(')')
    funcs = left[:l_right].split('(')[:-1]
    left_elements = getall(0, "(* ", [], funcs, fnames)
    r_right = right.find(')')
    funcs = right[:r_right].split('(')[:-1]
    ineq = '(and '
    right_elements = getall(0, "(* ", [], funcs, fnames)
    ineqs = []
    external_prev = []
    for i in left_elements:
        elems = i[1:-1].split(" ")[1:]
        prev = []
        for el in elems:
            width = 0
            if 'b' in el:
                width = 1
            else:
                width = 2
            m = expandToMatrix(el, width)
            if prev == []:
                prev = m
            else:
                prev = arctic_mult(prev, m)
        if external_prev == []:
            external_prev = prev
        else:
            external_prev = arctic_sum_1x1(external_prev, prev)
    r_external_prev = []
    for i in right_elements:
        elems = i[1:-1].split(" ")[1:]
        prev = []
        for el in elems:
            width = 0
            if 'b' in el:
                width = 1
            else:
                width = 2
            m = expandToMatrix(el, width)
            if prev == []:
                prev = m
            else:
                prev = arctic_mult(prev, m)
        if r_external_prev == []:
            r_external_prev = prev
        else:
            r_external_prev = arctic_sum_1x1(r_external_prev, prev)
    for i in range(len(external_prev)):
        for j in range(len(external_prev[0])):
            ineq += f'(arcgg {external_prev[i][j]} {r_external_prev[i][j]}) '
    return ineq[:-1] +' )'





def main():
    global toDeclare
    lefts, rights = input()
    l = generate(lefts, "left")
    r = generate(rights, "right")
    ineqs = []

    for i in range(len(lefts)):
        first = generateFirstInequality(lefts[i], rights[i])
        second = generateSecondInequality(lefts[i], rights[i])
        ineqs.append(first)
        ineqs.append(second)

    formSMT2(ineqs)

    print(fnames)


if __name__ == '__main__':
    print('Пример ввода: f(x) -> f(g(x))\n'
          'Когда поступает пустая строка, ввод считается завершенным')

    main()
    print('__________________________________________________________________________________________________________________________________________________________')


