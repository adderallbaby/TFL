import random
import StateEliminator

class Node:
    def __init__(self, data, stars, left=None, right=None):
        self.val = data
        self.under = stars
        self.left = left
        self.right = right


leftover = 0
alphabet = []
operator = []
everything = []
epsilon = []
maxlevel = 0


def generate(node):
    global leftover
    if leftover == 0:
        node.val = alphabet[random.randint(0, len(alphabet) - 1)]
        return
    elif leftover == 1 or leftover == 2:
        leftover -= 1
        node.val = alphabet[random.randint(0, len(alphabet) - 1)]
    else:
        if node.val is None:
            node.val = everything[random.randint(0, len(everything) - 1)]
        if node.val == '*':
            node.left = Node(everything[random.randint(0, len(everything) - 2)], node.under + 1)
            leftover -= 1
            generate(node.left)
        elif node.val == '#' or node.val == '·':
            if node.under < maxlevel:
                node.left = Node(everything[random.randint(0, len(everything) - 1)], node.under)
                node.right = Node(everything[random.randint(0, len(everything) - 1)], node.under)
            else:
                node.left = Node(everything[random.randint(0, len(everything) - 2)], node.under)
                node.right = Node(everything[random.randint(0, len(everything) - 2)], node.under)
            leftover -= 2
            generate(node.left)
            generate(node.right)
        elif node.val == '|':
            if node.under < maxlevel:
                node.left = Node(epsilon[random.randint(0, len(epsilon) - 1)], node.under)
                node.right = Node(epsilon[random.randint(0, len(epsilon) - 1)], node.under)
            else:
                node.left = Node(epsilon[random.randint(0, len(epsilon) - 2)], node.under)
                node.right = Node(epsilon[random.randint(0, len(epsilon) - 2)], node.under)
            leftover -= 2
            generate(node.left)
            generate(node.right)


def inorder(root):
    if root is None:
        return ''
    if not root.val == "·":
        out = inorder(root.left) + root.val + inorder(root.right)
    else:
        out = inorder(root.left) + inorder(root.right)

    if root.val in '|#*':
        return '(' + out + ')'
    return out


def main():
    global alphabet, operator, everything, leftover, epsilon, maxlevel

    leftover = 7
    maxlevel = 3

    characters = ['a', 'b', 'c', 'd', 'e']
    alphabet = characters[:random.randint(1, 5)]
    operator = ['|', '#', '·', '*']

    everything = []
    for i in alphabet:
        everything.append(i)
        epsilon.append(i)
    for i in operator:
        epsilon.append(i)
        everything.append(i)

    epsilon[len(epsilon) - 1] = 'ε'
    epsilon.append('*')

    node = Node(operator[random.randint(0, 3)], 0)
    generate(node)
    
    return inorder(node)


if __name__ == '__main__':
    regex = main()
    alphabet = ''
    print(regex)
    for i in regex:
        if i.isalpha():
            alphabet+=i
    print(regex, StateEliminator.main(alphabet, regex))
