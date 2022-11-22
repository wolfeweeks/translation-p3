from scanner import scanner
import sys
import node

tk = None
f = None

def printError(expect):
    global tk
    print('PARSER ERROR: On line ' + str(tk.line) + ': expected ' + str(expect) + ' but received \'' + tk.instance + '\'')

def RO(): # <RO> -> ++ | <= | -- | >= | = | %
    global tk
    global f

    n = node.Node('RO')

    if tk.type in ['++tk', '<=tk', '--tk', '>=tk', '=tk', '%tk']:
        n.addToken(tk.instance, tk.line)
        tk = scanner(f)
        return n
    else:
        printError('one of \'++\', \'--\', \'<=\', \'>=\', \'=\', or \'%\'')
        sys.exit()


def assign(): # <assign> -> ID == <expr>
    global tk
    global f

    n = node.Node('assign')

    if tk.type == 'IDtk':
        n.addToken(tk.instance, tk.line)
        tk = scanner(f)
        if tk.type == '==tk':
            n.addToken(tk.instance, tk.line)
            tk = scanner(f)
            n.addChild(expr())
            return n
        else:
            printError('\'==\'')
            sys.exit()
    else:
        printError('Identifier')
        sys.exit()


def loop(): # <loop> -> loop ( <expr> <RO> <expr> ) <stat>
    global tk
    global f

    n = node.Node('loop')

    if tk.type == 'LOOPtk':
        tk = scanner(f)
        if tk.type == '(tk':
            tk = scanner(f)
            n.addChild(expr())
            n.addChild(RO())
            n.addChild(expr())
            if tk.type == ')tk':
                tk = scanner(f)
                n.addChild(stat())
                return n
            else:
                printError('\')\'')
                sys.exit()
        else:
            printError('\'(\'')
            sys.exit()
    else:
        printError('\'loop\'')
        sys.exit()


def ifFunc(): # <if> -> fork ( <expr> <RO> <expr> ) then <stat>
    global tk
    global f

    n = node.Node('if')

    if tk.type == 'FORKtk':
        tk = scanner(f)
        if tk.type == '(tk':
            tk = scanner(f)
            n.addChild(expr())
            n.addChild(RO())
            n.addChild(expr())
            if tk.type == ')tk':
                tk = scanner(f)
                if tk.type == 'THENtk':
                    tk = scanner(f)
                    n.addChild(stat())
                    return n
                else:
                    printError('\'then\'')
                    sys.exit()
            else:
                printError('\')\'')
                sys.exit()
        else:
            printError('\'(\'')
            sys.exit()
    else:
        printError('\'fork\'')
        sys.exit()


def out(): # <out> -> print ( <expr> )
    global tk
    global f

    n = node.Node('out')

    if tk.type == 'PRINTtk':
        tk = scanner(f)
        if tk.type == '(tk':
            tk = scanner(f)
            n.addChild(expr())
            if tk.type == ')tk':
                tk = scanner(f)
                return n
            else:
                printError('\')\'')
                sys.exit()
        else:
            printError('\'(\'')
            sys.exit()
    else:
        printError('\'print\'')
        sys.exit()


def inFunc(): # <in> -> scan ID
    global tk
    global f

    n = node.Node('in')

    if tk.type == 'SCANtk':
        tk = scanner(f)
        if tk.type == 'IDtk':
            n.addToken(tk.instance, tk.line)
            tk = scanner(f)
            return n
        else:
            printError('Identifier')
            sys.exit()
    else:
        printError('\'scan\'')
        sys.exit()


def stat(): # <stat> -> <in> ; | <out> ; | <block> | <if> ; | <loop> ; | <assign> ;
    global tk
    global f

    n = node.Node('stat')

    if tk.type == 'SCANtk':
        n.addChild(inFunc())
        if tk.type == ';tk':
            tk = scanner(f)
            return n
        else:
            printError('\';\'')
            sys.exit()
    elif tk.type == 'PRINTtk':
        n.addChild(out())
        if tk.type == ';tk':
            tk = scanner(f)
            return n
        else:
            printError('\';\'')
            sys.exit()
    elif tk.type == 'FORKtk':
        n.addChild(ifFunc())
        if tk.type == ';tk':
            tk = scanner(f)
            return n
        else:
            printError('\';\'')
            sys.exit()
    elif tk.type == 'LOOPtk':
        n.addChild(loop())
        if tk.type == ';tk':
            tk = scanner(f)
            return n
        else:
            printError('\';\'')
            sys.exit()
    elif tk.type == 'IDtk':
        n.addChild(assign())
        if tk.type == ';tk':
            tk = scanner(f)
            return n
        else:
            printError('\';\'')
            sys.exit()
    elif tk.type == 'BEGINtk':
        n.addChild(block())
        return n
    else:
        printError('one of \'begin\', \'scan\', \'print\', \'fork\', \'loop\', or Identifier')
        sys.exit()


def mStat(): # <mStat> -> empty | <stat> <mStat>
    global tk
    global f

    n = node.Node('mStat')

    if tk.type in ['BEGINtk', 'IDtk', 'SCANtk', 'PRINTtk', 'FORKtk', 'LOOPtk']:
        n.addChild(stat())
        n.addChild(mStat())
        return n
    else: # follow should be end
        return


def stats(): # <stats> -> <stat> <mStat>
    global tk
    global f

    n = node.Node('stats')

    if tk.type in ['BEGINtk', 'IDtk', 'SCANtk', 'PRINTtk', 'FORKtk', 'LOOPtk']:
        n.addChild(stat())
        n.addChild(mStat())
        return n
    else:
        printError('one of \'begin\', \'scan\', \'print\', \'fork\', \'loop\', or Identifier')
        sys.exit()


def R(): # <R> -> [ <expr> ] | ID | NUM
    global tk
    global f

    n = node.Node('R')

    if tk.type == '[tk':
        tk = scanner(f)
        n.addChild(expr())
        if tk.type == ']tk':
            tk = scanner(f)
            return n
        else:
            printError('\']\'')
            sys.exit()
    elif tk.type == 'IDtk':
        n.addToken(tk.instance, tk.line)
        tk = scanner(f)
        return n
    elif tk.type == 'NUMtk':
        n.addToken(tk.instance, tk.line)
        tk = scanner(f)
        return n
    else:
        printError('one of Identifier, Integer, or \'[\'')
        sys.exit()


def M(): # <M> -> -- <M> | <R>
    global tk
    global f

    n = node.Node('M')

    if tk.type == '--tk':
        n.addToken(tk.instance, tk.line)
        tk = scanner(f)
        n.addChild(M())
        return n
    elif tk.type in ['IDtk', 'NUMtk', '[tk']:
        n.addChild(R())
        return n
    else:
        printError('one of Identifier, Integer, \'--\', or \'[\'')
        sys.exit()


def N(): # <N> -> <M> / <N> | <M> * <N> | <M>
    global tk
    global f

    n = node.Node('N')

    if tk.type in ['IDtk', 'NUMtk', '--tk', '[tk']:
        n.addChild(M())
        if tk.type == '/tk' or tk.type == '*tk':
            n.addToken(tk.instance, tk.line)
            tk = scanner(f)
            n.addChild(N())
            return n
        else: # follow of M should be ;, ++, --, ], ), <=, >=, =, or %
            return n
    else:
        printError('one of Identifier, Integer, \'--\', or \'[\'')
        sys.exit()


def A(): # <A> -> <N> -- <A> | <N>
    global tk
    global f

    n = node.Node('A')

    if tk.type in ['IDtk', 'NUMtk', '--tk', '[tk']:
        n.addChild(N())
        if tk.type == '--tk':
            n.addToken(tk.instance, tk.line)
            tk = scanner(f)
            n.addChild(A())
            return n
        else: # follow of N should be ;, ++, ], ), <=, >=, =, or %
            return n
    else:
        printError('one of Identifier, Integer, \'--\', or \'[\'')
        sys.exit()


def expr(): # <expr> -> <A> ++ <expr> | <A>
    global tk
    global f

    n = node.Node('expr')

    if tk.type in ['IDtk', 'NUMtk', '--tk', '[tk']:
        n.addChild(A())
        if tk.type == '++tk':
            n.addToken(tk.instance, tk.line)
            tk = scanner(f)
            n.addChild(expr())
            return n
        else: # follow of A should be ;, --, ], ), <=, >=, =, or %
            return n
    else:
        printError('one of Identifier, Integer, \'--\', or \'[\'')
        sys.exit()


def vars(): # <vars> -> empty | var ID : NUM ; <vars>
    global tk
    global f

    n = node.Node('vars')

    if tk.type == 'VARtk':
        tk = scanner(f)
        if tk.type == 'IDtk':
            n.addToken(tk.instance, tk.line)
            tk = scanner(f)
            if tk.type == ':tk':
                tk = scanner(f)
                if tk.type == 'NUMtk':
                    n.addToken(tk.instance, tk.line)
                    tk = scanner(f)
                    if tk.type == ';tk':
                        tk = scanner(f)
                        n.addChild(vars())
                        return n
                    else:
                        printError('\';\'')
                        sys.exit()
                else:
                    printError('Integer')
                    sys.exit()
            else:
                printError('\':\'')
                sys.exit()
        else:
            printError('Identifier')
            sys.exit()
    else: # follow should be begin, ID, scan, print, fork, or loop
        return


def block(): # <block> -> begin <vars> <stats> end
    global tk
    global f

    n = node.Node('block')

    if tk.type == 'BEGINtk':
        tk = scanner(f)
        n.addChild(vars())
        n.addChild(stats())
        if tk.type == 'ENDtk':
            tk = scanner(f)
            return n
        else:
            printError('\'end\'')
            sys.exit()
    else:
        printError('\'begin\'')
        sys.exit()


def program(): # <program> -> <vars> <block>
    global tk
    global f

    n = node.Node('program')
    
    if tk.type == 'VARtk':
        n.addChild(vars())
        n.addChild(block())
        return n
    elif tk.type == 'BEGINtk':
        n.addChild(block())
        return n
    else:
        printError('either \'var\' or \'begin\'')
        sys.exit()


def parser(file):
    global tk
    global f

    f = file

    tk = scanner(f)

    root = None

    root = program()

    if tk.type == 'EOFtk':
        return root
    else:
        printError('\'EOF\'')
        sys.exit()
