import sys
import os
import stat
from my_parser import parser
from semantics import staticSemantics

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('too many command line arguments')
        sys.exit()

    if len(sys.argv) == 2:
        filename = sys.argv[-1] + '.cs4280'
        if not os.path.exists(filename):
            print('the file \'' + filename + '\' does not exist')
            sys.exit()

        f = open(filename, 'r')
        tree = parser(f)
        staticSemantics(tree, 0)
        print('semantics ok')
        f.close()

    else:
        # code to check if stdin is redirected or not found at link below
        # https://stackoverflow.com/questions/13442574/how-do-i-determine-if-sys-stdin-is-redirected-from-a-file-vs-piped-from-another
        mode = os.fstat(sys.stdin.fileno()).st_mode
        
        # if stdin is from a redirect
        f = open('tmp', 'w+')
        if stat.S_ISREG(mode):
            for line in sys.stdin:
                f.write(line)
        else: # if stdin is through the console
            try:
                print('Enter words and lines and press Ctrl-D (Ctrl-Z on Windows) when finished')
                while True:
                    line = raw_input()  # get user input
                    if line == '':
                        line = '\n'
                    if line[-1] != '\n':
                        line += '\n'
                    f.write(line)
            except EOFError:
                pass
                #remove last "new line" character from file
                # f.seek(0,2)
                # f.seek(f.tell() - 2,0)
                # f.truncate()
            
        f.seek(0,0)

        # sc.testScanner(f) # call the test scanner
        tree = parser(f)
        staticSemantics(tree, 0)
        print('semantics ok')
        f.close()

        f.close()
        os.remove('tmp')

# f = open('./testFile', 'r')

# tree = parser(f)
# printPreorder(tree, 0)

# f.close()
