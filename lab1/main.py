# This is a sample Python script.
a_iterator = 0
b_iterator = 0
import sys
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
            level -=1
        elif char == separator and level == 1:
            t.append(line[prev:i].strip())
            prev = i + 1
    t.append(line[prev:].strip())
    return t

def generateLinear(x):
    global a_iterator, b_iterator
    linear = "(+ "
    for i in x:
        linear += f'(* a{a_iterator} {i}) '
        a_iterator += 1
    linear += f"b{b_iterator})"
    b_iterator += 1
    return linear

def generateSingle(args):
    if len(args) == 1 and not "(" in args[0]:
        return args[0]
    linear = generateLinear(args)
    for arg in args:
        if "(" in arg:
            cur = generateSingle(tuple(splitOnSameLvl(
                arg[arg.find('(') + 1:-1], ",")))
            linear = linear.replace(arg, cur)
    return linear

def generate(functions):
    formed = []
    for function in functions:
        left = function.find("(") + 1
        right = function.rfind(")")
        print(tuple(splitOnSameLvl(function[left:right], ",")))
        formed.append(generateSingle(tuple(splitOnSameLvl(function[left:right], ","))))
    return formed
def main():
    lefts, rights = input()
    l = generate(lefts)
    for i in l:
        print(i)
if __name__ == '__main__':
    main()
