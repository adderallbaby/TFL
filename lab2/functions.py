import deriv_generator
#((((a#a))*((((a#a))*|a))*)|(((a((a#a))*)|ε)((((a#a))*|a))*))
#(((((a((a#a))*)((((a#a))*|a))*)|(((a((a#a))*)|ε)((((a#a))*|a))*))|(((a#a))*((((a#a))*|a))*))|
#(((a((a#a))*)|ε)((((a#a))*|a))*))
def validParentheses(string):
    stack = []
    for symbol in string:
        if symbol == '(':
            stack.append('(')
        elif symbol == ')':
            if len(stack) < 1:
                return False 
            stack.pop()

    return len(stack) == 0
def prettyInorder(root):
    if root is None:
        return ''
    if root.val == '*':
        return "("+prettyInorder(root.left) + ")*"
    if root.val != '·':
        out = prettyInorder(root.left) + root.val + prettyInorder(root.right)
    else: 
        out = prettyInorder(root.left) +  prettyInorder(root.right)
    if root.val in '#|':
        return '(' + out + ')'

    return out
def getValidParentheses(stack, out):
    while len(stack) > 0 and stack[-1] != "(":
        out.append(stack.pop())
    
def sameTree(q, p):
    if (q == None and p == None):
        return True

    if (q == None or p == None):
        return False

    if (q.val != p.val):
        return False
    if (q.val == '·' or p.val == '·') or (q.val == '#' or p.val == '#'):
        return (sameTree(p.left, q.left) and sameTree(p.right, q.right))
    return (sameTree(p.left, q.left) and sameTree(p.right, q.right)) or (sameTree(p.left, q.right) and sameTree(p.right, q.left))
#((((a)*#b)|(b#(a)*))|((ab)#(a)*))
def containsSameTree(forest, tree):
    for i in forest:
        if (sameTree(i,tree)):
            return i
    return tree

def getHeight(node, level):
    if node == None:
        return level
    hleft = getHeight(node.left, level +1)
    hright = getHeight(node.right, level+1)
    return max(hleft, hright)
def makeLeftSided(node):

    if node == None :
        return  node   #if  node.val == '·':
    #    return node
    if node.val == '|' and node.right.val == '|':
        #print(deriv_generator.inorder(node))

        #print("HERE")
        node = rotate_left(node)
    #print(deriv_generator.inorder(node))
    node.left = makeLeftSided(node.left)
    node.right = makeLeftSided(node.right)
    return node
#           |
#((a)*#b)              |
#              (b#(a)*)     ((ab)#(a)*)
#(((a)*#b)|((b#(a)*)|((ab)#(a)*))
def rotate_left(root):
    rotated_root = root.right 
    if not rotated_root:
        return root 
    try: 
        temp = rotated_root.left 
    except:
        print('something prolly wrong')
    rotated_root.left = root 
    root.right = temp 
    return rotated_root
