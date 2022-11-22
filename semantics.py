import sys

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, string):
        self.stack.append(string)

    def pop(self):
        self.stack.pop()

    def find(self, string):
        for i in range(len(self.stack)):
            if self.stack[-(i + 1)] == string:
                return i
        return -1


stack = Stack()
varCounts = {}

def staticSemantics(root, blockNo):
    global stack
    global varCounts

    def isId(token):
        if token[0] in 'abcdefghijklmnopqrstuvwxyz': return True
        return False

    if blockNo not in varCounts.keys():
        varCounts[blockNo] = 0
    
    if root:
        if root.nonterminal == 'vars':
            if varCounts[blockNo] > 0:
                find = stack.find(root.tokens[0])
                if find >= 0 and find < varCounts[blockNo]:
                    print('SEMANTICS ERROR: On line ' + str(root.tokenLines[0]) + ': multiple definitiions of \'' + root.tokens[0] + '\'')
                    sys.exit()
            
            stack.push(root.tokens[0])
            varCounts[blockNo] += 1
        else:
            if len(root.tokens) > 0:
                for i in range(len(root.tokens)):
                    if isId(root.tokens[i]) and stack.find(root.tokens[i]) == -1:
                        print('SEMANTICS ERROR: On line ' + str(root.tokenLines[i]) + ': identifier \'' + root.tokens[i] + '\' was not instantiated')
                        sys.exit()
        
        if root.children is not None:
            for child in root.children:
                if child and child.nonterminal == 'block':
                    staticSemantics(child, blockNo + 1)
                else:
                    staticSemantics(child, blockNo)

    if root.nonterminal in ['block', 'program']:    
        for i in range(varCounts[blockNo]):
            stack.pop()