import sys
import functions
#((((a)*|ε)#a)|((a)*|a))
#(((((a)*|ε)#a)|(a)*)|a)
#(((((a)*#a)|((a)*|ε))|(a)*)|ε)
#(((b#(a)*)|(b#(a)*))|((ab)#(a)*))
operations = {'(': 0, '#': 1, '|': 2, '·': 3, '*': 4}
def makeConcat(src):
    if not src:
        return 'ε'
    output = []
    for i in range(0,len(src)):
        if i > 0 and not(src[i] in '#|)*' or src[i - 1] in '(|#'):
            output.append('·')
        output.append(src[i])
    return ''.join(output)

def inorder(root):
    if root is None:
        return ''
    if root.val == '*':
        return "("+inorder(root.left) + ")*"
    if root.val != '·':
        out = inorder(root.left) + root.val + inorder(root.right)
    else: 
        out = inorder(root.left) +  inorder(root.right)

    if root.val in '·#|*':
        return '(' + out + ')'
    return out
class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.val = data
        self.left = left
        self.right = right
c = 0
def postorder(root):
    global c
    if root is None:
        return


    postorder(root.left)
    postorder(root.right)
    #print(root.val)
    #print(inorder(root))
    if root.val in '|·*#':
        if root.val == '|':
            

            if root.left.val.isalpha() and root.right.val.isalpha():
                aa = []
                aa.append(root.left.val)
                aa.append(root.right.val)
                aa.sort()
                root.left.val = aa[0]
                root.right.val = aa[1]
            if root.left.val == '∅':
                root.val = root.right.val
                root.left = root.right.left
                root.right = root.right.right

            elif root.right.val == '∅':
                root.val = root.left.val
                root.right = root.left.right
                root.left = root.left.left

            elif functions.sameTree(root.right, root.left):
                #print("HERE is the same---")
                #print(inorder(root))
                
                dnode = clone(root.left)
                root.val = dnode.val
                root.left = dnode.left
                root.right = dnode.right 
                
                #temp = root.left 
                #root.right = None 
                #root = temp
                #print(inorder(root))
            elif (root.left.val == '|' and (functions.sameTree(root.right, root.left.left) or functions.sameTree(root.right, root.left.right))) or functions.sameTree(root.right, root.left) :
                #print("HERE")
                #print(inorder(root)) 
                temp = clone(root.left)
                #print(temp.val, 'val')
                #root.right = None 
                #root = None 
                root.left = temp.left 
                root.right = temp.right
                root.val = temp.val
                #print(inorder(root)) 


        elif root.val == '·':
            if root.left.val == '∅' or root.right.val == '∅':
                root.val = '∅'
                root.left = None
                root.right = None


            elif root.right.val == 'ε':
                root.val = root.left.val
                root.left = root.left.left
                root.right = root.left.right

            elif root.left.val == 'ε':

                root.val = root.right.val
                root.left = root.right.left
                root.right = root.right.right
        elif root.val == '#':
            if root.left.val == 'ε':
                # root = root.right
                root.val = root.right.val
                root.left = root.right.left
                root.right = root.right.right
            elif root.right.val == 'ε':
                # root = root.left
                root.val = root.left.val
                root.right = root.left.right
                root.left = root.left.left
            elif root.right.val == '∅' or root.left.val == '∅':
                #print("HERE")
                root.val = '∅'
                root.left = None
                root.right = None
        elif root.val == '*':
            if root.left.val =='*':
                dnode = clone(root.left.left)
                root.left = dnode

def getPostfix(exp):
    stack = []
    output = []
    for c in exp:
        if c.isalpha():
            output.append(c)
        elif c == "(":
            stack.append(c)
        elif c == ")":
            while len(stack) > 0 and stack[-1] != "(":
                output.append(stack.pop())
            else:
                stack.pop()
        else:
            while len(stack) > 0 and operations[stack[-1]] >= operations[c]:
                output.append(stack.pop())
            stack.append(c)

    while len(stack) > 0:
        output.append(stack.pop())
    return "".join(output)

def getBinaryTree(postfix):
    if not postfix:
        return
    stack = []
    #print(postfix, 'postfix')
    for c in postfix:
        if c in "#|·":
            r, l = stack.pop(), stack.pop()
            stack.append(TreeNode(c, l, r))
        elif c in "*":
            l = stack.pop()
            stack.append(TreeNode(c, l))
        else:
            stack.append(TreeNode(c))

    return stack[-1]


def clone(node):
    if node is None:
        return None
    return TreeNode(node.val, clone(node.left), clone(node.right))


def nullable(node):
    if node is None:
        return False
    elif node.val == 'ε':
        return True
    #elif node.val == '∅':
    #    return False
    elif node.val == '*':
        return True
    elif node.val == '|':
        return nullable(node.left) or nullable(node.right)
    elif node.val == '·' or node.val == '#':
        return nullable(node.left) and nullable(node.right)

    else:
        return False

def deriv(root, c):
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        #print(inorder(node))
        if node is None or node.val == '∅':  
            continue
        elif node.val == 'ε':  
            node.val = '∅'
        elif node.val == "|":
            stack.append(node.left)
            stack.append(node.right)
        elif node.val == "·":
            if nullable(node.left):
                node.val = "|"
                dnode = TreeNode("·", node.left, node.right)
                node.left = dnode
                node.right = clone(dnode.right)
                stack.append(node.left.left)
                stack.append(node.right)
            else:
                stack.append(node.left)
        elif node.val == c:  
            node.val = 'ε'
        elif node.val == "*":  
            star = clone(node)
            node.val = "·"
            node.right = star
            #print(inorder(node.left))
            stack.append(node.left)

        ###(a·b)#(c·d)
        ###((∅·b)#(c·d)|(a·b)#(∅·d))
        ###False

        elif node.val == "#":
            # ((a#b)#b)* = ((a#b)#b)((a#b)#b)* = b#b((a#b)#b)* 
            # (a#b)#b= ∂ₐ(a#b) # b| (a#b) #∂ₐ(b) = b#b
            #∂ₐ(a#b) = b
            node.val = '|'
            llnode = TreeNode('#',node.left, node.right)
            dnode= TreeNode('#', clone(node.left), clone(node.right))

            node.left = llnode 
            node.right = dnode
            #print(inorder(node), 'inorder', node.left.left.val)
            #print(inorder(node.right),'inorder', node.right.right.val)
            stack.append(node.left.left)
            stack.append(node.right.right)
# node.left =   # print("-------------------------------")  # print(left_node.left, left_node.right) 

            # print(right_node.left , right_node.right)  # print("-------------------------------")

            # stack.append(node)
        else:
            node.val = '∅'  
    return root

def getDerived(regex, c):
    #print(regex)
    #print(getPostfix(makeConcat(regex)), 'this is it')
    node =(getBinaryTree(getPostfix(makeConcat(regex))))
    node = functions.makeLeftSided(node)

    postorder(node)


    result = inorder(node)
    
    #print(result, "RES1")

    #print(node.val)
    #print(node.left.val)
    a = deriv(node, c)
    #
    result = inorder(a)

    postorder(a)
    a = functions.makeLeftSided(a)
    postorder(a)
    result = inorder(a)
    #print(result, "RES", c)
    return result

if __name__ == "__main__":

    getDerived(sys.argv[1], sys.argv[2])

