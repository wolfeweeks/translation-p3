class Node:
    def __init__(self, nonterminal):
        self.nonterminal = nonterminal
        self.tokens = []
        self.tokenLines = []
        self.children = None

    def addToken(self, token, line):
        self.tokens.append(token)
        self.tokenLines.append(line)

    def addChild(self, child):
        if child is None:
            return
        if self.children is None:
            self.children = []
        self.children.append(child)

    def write(self, depth):
        line = ''
        for i in range(depth):
            line += '  '
        line += '<' + self.nonterminal + '>'
        for token in self.tokens:
            line += ' ' + str(token)
        print(line)
