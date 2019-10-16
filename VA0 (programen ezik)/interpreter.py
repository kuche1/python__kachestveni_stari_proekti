#'v1.0.0'
import copy





class func():
    name = []
    value = []
    varnum = 0
    def add(self, name, value):
        self.name.append(name)
        self.value.append(value)
    def get(self, name):
        num = self.name.index(name)
        return self.value[num]
    def rem(self, name):
        num = self.name.index(name)
        del self.name[num]
        del self.value[num]
func = func()
#func.add('', [])
func.add('newline', [['return','\n']])
func.add('semicolon', [['return',';']])
func.add('space', [['return',' ']])

BREAK = 0
def execline(line):
    global BREAK
    if line[0] == '' or line[0][0] == '#':
        pass
    elif line[0] == '/_float_float':
        return line[1] / line[2]
    #a
    elif line[0] == 'add_float_float':
        return line[1] + line[2]
    #b
    elif line[0] == 'break':
        BREAK += line[1]
    elif line[0] == 'break2if=':
        if line[1] == line[2]:
            BREAK += 2
    elif line[0] == 'break2if>0':
        if line[1] > 0:
            BREAK += 2
    #d
    elif line[0] == 'del':
        func.rem(line[1])
    #f
    elif line[0] == 'fst':
        return line[1][0]
    elif line[0] == 'float':
        return float(line[1])
    #i
    elif line[0] == 'import':
        execfile(line[1])
    elif line[0] == 'input':
        return input()
    #l
    elif line[0] == 'len':
        return len(line[1])
    #p
    elif line[0] == 'putch':
        if len(line[1]) > 1:print('putch is used for puting characters, not strings:');print(line[1]);raise
        print(line[1], end='')
    #r
    elif line[0] == 'return':
        return line[1]
    #s
    elif line[0] == 'str':
        return str(line[1])
    #t
    elif line[0] == 'tail':
        return line[1][1:]
    elif line[0] == 'type':
        return type(line[1]).__name__
    else:
        if line[0] in func.name:
            value = copy.deepcopy(func.get(line[0]))
            for x, funcline in enumerate(value):
                for y, arg in enumerate(funcline):
                    if arg == 'arg1':
                        value[x][y] = line[1]
                    elif arg == 'arg2':
                        value[x][y] = line[2]
                    elif arg == 'arg3':
                        value[x][y] = line[3]
                
            for funcline in value:
                while ':' in funcline:
                    for y in range(len(funcline)-1,-1,-1):
                        if funcline[y] == ':':
                            returned = execline(funcline[y+1:])
                            funcline[y:] = returned if type(returned) == list else [returned]
                            break
                toreturn = execline(funcline + line[1:])
                if BREAK>0:
                    BREAK -= 1
                    return None
                if toreturn != None:
                        return toreturn
        else:
            kot = line[1:]
            value = []
            while ';' in kot:
                start = 0
                for x, arg in enumerate(kot):
                    if arg == ';':
                        value.append(kot[start:x])
                        start = x
                        kot = kot[x+1:]
                        break
            value.append(kot)
            print('Set: %s'%(line[0]))
            func.add(line[0], value)

def execfile(fname,debug=True):
    f = open(fname, 'r')
    code = f.read()
    f.close()
    code = code.split('\n')
    for x in range(len(code)):
        code[x] = code[x].split(' ')
    for linenum, line in enumerate(code):
        if debug:print('%s: %s'%(linenum+1, line))
        execline(line)

execfile('init.txt',False)
execfile('aa.txt')
while True:
    print(execline(input('>>>').split(' ')))
