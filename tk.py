def isKeyword(instance):
    if instance == 'begin':
        return True
    if instance == 'end':
        return True
    if instance == 'loop':
        return True
    if instance == 'void':
        return True
    if instance == 'var':
        return True
    if instance == 'exit':
        return True
    if instance == 'scan':
        return True
    if instance == 'print':
        return True
    if instance == 'main':
        return True
    if instance == 'fork':
        return True
    if instance == 'then':
        return True
    if instance == 'let':
        return True
    if instance == 'data':
        return True
    if instance == 'func':
        return True
    return False


def keywordTk(instance):
    if instance == 'begin':
        return 'BEGINtk'
    if instance == 'end':
        return 'ENDtk'
    if instance == 'loop':
        return 'LOOPtk'
    if instance == 'void':
        return 'VOIDtk'
    if instance == 'var':
        return 'VARtk'
    if instance == 'exit':
        return 'EXITtk'
    if instance == 'scan':
        return 'SCANtk'
    if instance == 'print':
        return 'PRINTtk'
    if instance == 'main':
        return 'MAINtk'
    if instance == 'fork':
        return 'FORKtk'
    if instance == 'then':
        return 'THENtk'
    if instance == 'let':
        return 'LETtk'
    if instance == 'data':
        return 'DATAtk'
    if instance == 'func':
        return 'FUNCtk'


def stateToTk(state, instance):
    if state == 101:
        if isKeyword(instance):
            return keywordTk(instance)
        return 'IDtk'
    if state == 102:
        return '=tk'
    if state == 104:
        return '<=tk'
    if state == 106:
        return '>=tk'
    if state == 107:
        return '==tk'
    if state == 108:
        return ':tk'
    if state == 110:
        return '++tk'
    if state == 112:
        return '--tk'
    if state == 113:
        return '*tk'
    if state == 114:
        return '/tk'
    if state == 115:
        return '%tk'
    if state == 116:
        return '.tk'
    if state == 117:
        return '(tk'
    if state == 118:
        return ')tk'
    if state == 119:
        return ',tk'
    if state == 120:
        return '{tk'
    if state == 121:
        return '}tk'
    if state == 122:
        return ';tk'
    if state == 123:
        return '[tk'
    if state == 124:
        return ']tk'
    if state == 125:
        return 'NUMtk'
    if state == 126:
        return 'EOFtk'

class Token:
    # def __init__(self)
    def addChar(self, char):
        try:
            self.instance += char
        except:
            self.instance = char

    
    def setType(self, state):
        self.type = stateToTk(state, self.instance)


    def printTk(self):
        print(str(stateToTk(self.state, self.instance)) + ' | ' + self.instance + ' | ' + str(self.line))