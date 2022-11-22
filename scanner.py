import sys

import tk as token

fsa = [
    # ws low  up num   =   <   >   :   +   -   *   /   %   .   (   )   ,   {   }   ;   [   ] eof
    [  0,  1, -1, 25,  2,  3,  5,  8,  9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,126], # 0 start
    [101,  1,  1,  1,101,101,101,101,101,101,101,101,101,101,101,101,101,101,101,101,101,101,101], # 1 id
    [102,102,102,102,  7,102,102,102,102,102,102,102,102,102,102,102,102,102,102,102,102,102,102], # 2 =
    [ -2, -2, -2, -2,  4, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2], # 3 <
    [104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104,104], # 4 <=
    [ -3, -3, -3, -3,  6, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3], # 5 >
    [106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106], # 6 >=
    [107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107], # 7 ==
    [108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108,108], # 8 :
    [ -4, -4, -4, -4, -4, -4, -4, -4, 10, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4], # 9 +
    [110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110], # 10 ++
    [ -5, -5, -5, -5, -5, -5, -5, -5, -5, 12, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5], # 11 -
    [112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112], # 12 --
    [113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113], # 13 *
    [114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114], # 14 /
    [115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115], # 15 %
    [116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116], # 16 .
    [117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117], # 17 (
    [118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118], # 18 )
    [119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119], # 19 ,
    [120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120], # 20 {
    [121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121], # 21 }
    [122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122], # 22 ;
    [123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123], # 23 [
    [124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124], # 24 ]
    [125,125,125, 25,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125], # 25 number
]

lineNo = 1


def charToColumn(char):
    global lineNo

    if char in ' \t\n#':
        return 0
    if char in 'abcdefghijklmnopqrstuvwxyz':
        return 1
    if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return 2
    if char in '0123456789':
        return 3
    if char == '=':
        return 4
    if char == '<':
        return 5
    if char == '>':
        return 6
    if char == ':':
        return 7
    if char == '+':
        return 8
    if char == '-':
        return 9
    if char == '*':
        return 10
    if char == '/':
        return 11
    if char == '%':
        return 12
    if char == '.':
        return 13
    if char == '(':
        return 14
    if char == ')':
        return 15
    if char == ',':
        return 16
    if char == '{':
        return 17
    if char == '}':
        return 18
    if char == ';':
        return 19
    if char == '[':
        return 20
    if char == ']':
        return 21
    if char == 'eof':
        return 22
    
    print('LEXICAL ERROR: unrecognized character on line ' + str(lineNo) + ': ' + char)
    sys.exit()


def filter(f):
    global lineNo

    c = f.read(1)

    if not c:
        c = 'eof'
    if c == '\n':
        lineNo += 1
    if c == '#':
        c1 = ''
        while True:
            c1 = f.read(1)
            if c1 == '#':
                break
            if not c1:
                print('LEXICAL ERROR: comment never closed')
                sys.exit()
            if c1 == '\n':
                lineNo += 1
    return c

def scanner(f):
    global lineNo
    # print

    tk = token.Token()

    state = 0
    while state < 100 and state >= 0:
        char = filter(f)

        if not hasattr(tk, 'line'):
            if state != 0:
                tk.line = lineNo

        state = fsa[state][charToColumn(char)]

        if state < 0:
            error = 'LEXICAL ERROR: On line ' + str(lineNo) + ': '
            if state == -1:
                error += 'word started with capital letter'
            elif state == -2:
                error += '< must be followed immediately by ='
            elif state == -3:
                error += '> must be followed immediately by ='
            elif state == -4:
                error += '+ must be followed immediately by +'
            elif state == -5:
                error += '- must be followed immediately by -'
            print(error)
            sys.exit()

        if state < 100 and state > 0:
            tk.addChar(char)
        if state > 100 and char != 'eof' and state != 126 and char != '#':
                if char == '\n':
                    lineNo -= 1
                f.seek(-1, 1)
        if state == 126:
            tk.addChar('EOF')
            tk.line = lineNo

    tk.state = state
    tk.setType(tk.state)

    return tk

    
def testScanner(f):
    while True:
        tk = scanner(f)
        tk.printTk()
        if tk.state == 126:
            break