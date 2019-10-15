print('KY$ [Version 2.6.2 (?)]')
print('Copyright (c) 2016 Troshiq Corporation. All rights reserved.')
print()
import os
import random
import subprocess
import sys
import time

class var():
    Name = []
    Value = []
    def add(self, name, value):
        if name in self.Name:
            self.Value[self.Name.index(name)] = value
        else:
            self.Name.append(name)
            self.Value.append(value)
    def value(self, name):
        if name in self.Name:
            return self.Value[self.Name.index(name)]

        if len(name) > 0:
            if name[0] == '#':
                return len(var.value(name[1:]))
            if name[0] == '$':
                return str(name[1:])
            if (name.count('[') == 1) and (name.count(']') == 1) and name[-1] == ']':
                if ':' in name[name.index('[')+1:-1]:
                    temp = name[name.index('[')+1:-1].split(':')
                    return self.value(name[:name.index('[')])[int(self.value(temp[0])):int(self.value(temp[1]))]
                else:
                    return self.value(name[:name.index('[')])[int(self.value(name[name.index('[')+1:-1]))]

        try:
            if '.' in name:
                name = float(name)
            else:
                name = int(name)
            return name
        except:
            return None
var = var()

class functions():
    Name = []
    Args = []
    Value = []
    def add(self, name, args, value):
        if name in self.Name:
            pos = self.Name.index(name)
            self.Args[pos] = args
            self.Value[pos] = value
        else:
            self.Name.append(name)
            self.Args.append(args)
            self.Value.append(value)
    def value(self, name):
        pos = self.Name.index(name)
        return self.Args[pos], self.Value[pos]
functions = functions()

def iz4islqvane(item1, item2, item3):
    if item2 == '==':
        return item1 == item3
    elif item2 == '!=':
        return item1 != item3
    elif item2 == '<=':
        return item1 <= item3
    elif item2 == '>=':
        return item1 >= item3
    elif item2 == '<':
        return item1 < item3
    elif item2 == '>':
        return item1 > item3
    elif item2 == '+':
        return item1 + item3
    elif item2 == '-':
        return item1 - item3
    elif item2 == '*':
        return item1 * item3
    elif item2 == '/':
        return item1 / item3
    elif item2 == '%':
        return item1 % item3
    elif item2 == '//':
        return item1 // item3
    elif item2 == '**':
        return item1 ** item3
    else:
        print('ERROR: math: unknown operator: %s' %(item2))
        raise

def executeCode(code):
    executingLine = 0
    while executingLine < len(code):
        curL = code[executingLine]

        if curL.count('{') != curL.count('}'):
            print('ERROR: count("{") != count("}")')
            print(executingLine)
            raise
        while '{' in curL:
            item = curL.index('{')
            ifs = 0
            for x in range(item, len(curL)):
                if curL[x] == '{':
                    ifs += 1
                elif curL[x] == '}':
                    ifs -= 1
                    if ifs == 0:
                        executeCode([curL[item+1:x]])
                        curL = list(curL)
                        curL = curL[:item] + curL[x+1:]
                        curL = ''.join(curL)
                        break
                    elif ifs < 0:
                        print('ERROR: incorrect usage of { and }')
                        print(currentLine)
                        raise
        
        curL = curL.split(';')
        for x in range(len(curL)):
            curL[x] = var.value(curL[x])
        
        if curL[0] == 'set': #slaga v {1} si4ko ot {2} do kraq (1 kum 1)
            var.add(curL[1], curL[2])
        #a
        elif curL[0] == 'add': #slaga v {1} sbora na {2} i {3}
            var.add(curL[1], curL[2] + curL[3])
        #b
        #c
        elif curL[0] == 'chr': #slaga v {1} keraktara, stoq6t zad {2} po askii
            var.add(curL[1], chr(curL[2]))
        elif curL[0] == 'com': #komentar
            executingLine = executingLine
        elif curL[0] == 'continue': #slaga6 go s ideqta da NE izleze6 ot if, a vmesto tva da se proveri na novo uslovieto, i ako e istina da se ispulni si4ko ot starta na ifa nadolu
            ifs = 0
            start = executingLine
            for x in range(len(code[:executingLine])-1, -1, -1):
                start -= 1
                if var.value(code[x].split(';')[0]) == 'endif':
                    ifs -= 1
                elif var.value(code[x].split(';')[0]) == 'if':
                    if ifs == 0:
                        executingLine = start - 1
                        break
                    ifs += 1
        #d
        elif curL[0] == 'decode': #slaga v {1} {2}, dekodirano po standart {3}
            var.add(curL[1], curL[2].decode(curL[3]))
        #e
        elif curL[0] == 'encode': #slaga v {1} {2}, kodirano po standart {3}
            var.add(curL[1], curL[2].encode(curL[3]))
        elif curL[0] == 'endfunc': #s tva si otbelqzva6 kraq na funkciqta
            executingLine = executingLine
        elif curL[0] == 'endif': #s tva si otbelqzva6 kraq na ifa
            executingLine = executingLine
        elif curL[0] == 'endtry': #s tva si otbelqzva6 kraq na try-a
            executingLine = executingLine
        elif curL[0] == 'execute': #se edno si napisal {1}, kato kod
            executeCode(strToCode(curL[1]))
        #f
        elif curL[0] == 'float': #slaga v {1} {2}, konventirano na ne cqlo 4islo
            var.add(curL[1], float(curL[2]))
        elif curL[0] == 'func': #prai6 si funkciq
            funcName = curL[1]
            funcArgs = curL[2:]
            funcValue = []
            ifs = 0
            end = executingLine
            item = True
            for line in code[executingLine+1:]:
                if var.value(line.split(';')[0]) == 'func':
                    ifs += 1
                elif var.value(line.split(';')[0]) == 'endfunc':
                    if ifs == 0:
                        item = False
                        break
                    ifs -= 1
                funcValue.append(line)
                end += 1
            if item:
                print('ERROR: vi6 si funkciite')
                print(executingLine)
                raise
            executingLine = end
            functions.add(funcName, funcArgs, funcValue)
        #g
        #h
        #i
        elif curL[0] == 'if': #ako {1} e istina (kompa go za4ita za "True") ispulnqva si4ko do endif, ina4e go skipva
            ifs = 0
            end = executingLine
            item = True
            for line in code[executingLine+1:]:
                if var.value(line.split(';')[0]) == 'if':
                    ifs += 1
                elif var.value(line.split(';')[0]) == 'endif':
                    if ifs == 0:
                        item = False
                        break
                    ifs -= 1
                end += 1
            if item:
                print('ERROR: ifovete si vi6')
                print(executingLine)
                raise
            if curL[1]:
                executingLine = executingLine
            else:
                executingLine = end
        elif curL[0] == 'import': #runva fil {1} (zapazvat se si4ki varuabali, funkcii)
            executeFile(curL[1])
        elif curL[0] == 'input': #slaga v {1} inputa na user-a
            var.add(curL[1], input(curL[2]))
        elif curL[0] == 'int': #slaga v {1} {2}, konventirano na cqlo 4islo
            var.add(curL[1], int(curL[2]))
        #j
        #k
        #l
        elif curL[0] == 'len': #slaga v {1} duljinata na {2}
            var.add(curL[1], len(curL[2]))
        elif curL[0] == 'list': #slaga v {1}  {2}, konventirano na lista
            var.add(curL[1], list(curL[2]))
        elif curL[0] == 'list.append': #dobavq {2} v kraq na listata {1},    gore dolu useless komanda, pri polojenie 4e ima6 list.index
            curL[1].append(curL[2])
        elif curL[0] == 'list.change': #item nomer {2} na listata {1} se promenq na {3}
            curL[1][curL[2]] = curL[3]
        elif curL[0] == 'list.del': #iztriva item nomer {2}, ot listata {1} (purviq item na listata ima nomer 0)
            del curL[1][curL[2]]
        elif curL[0] == 'list.insert': #dobavq {3}, na poziciq {2}, v lista {1}
            curL[1].insert(curL[2], curL[3])
        elif curL[0] == 'list.max': #slaga v {1} nai-golqmiq element ot listata {1}
            var.add(curL[1], max(curL[2]))
        elif curL[0] == 'list.min': #slaga v {1} nai-malkiq element ot listata {1}
            var.add(curL[1], min(curL[2]))
        elif curL[0] == 'list.split': #slaga v {1}  {2} kato lista, razdeleno po kriterii {3}
            var.add(curL[1], curL[2].split(curL[3]))
        #m
        elif curL[0] == 'math': #v {1} zapisva {2}{3}{4},    ako mu kaje6 1;$==;1 to 6a ti dade True,    ako mu kaje6 1;+;1 to 6a ti dade 2
            var.add(curL[1], iz4islqvane(curL[2], curL[3], curL[4]))
        #n
        elif curL[0] == 'None': #v {1} slaga None
            var.add(curL[1], None)
        #o
        elif curL[0] == 'ord': #slaga v {1} askii koda na {2}
            var.add(curL[1], ord(curL[2]))
        elif curL[0] == 'os.environ': #slaga v {1} edin vid direktoriq {2}. Primer: ako mu dade6 HOME, to 6a ti dade home directoriqta. Ako mu dade6 TEMP, to 6a ti dade temp direktoriqta
            var.add(curL[1], os.environ[curL[2]])
        elif curL[0] == 'os.getcwd': #slaga v {1} sega6nata working direktoriq
            var.add(curL[1], os.getcwd())
        elif curL[0] == 'os.getlogin': #slaga v {1} username-a na lognatiq user
            var.add(curL[1], os.getlogin())
        elif curL[0] == 'os.getpid': #slaga v {1} id-to na sega6niq proces
            var.add(curL[1], os.getpid())
        elif curL[0] == 'os.path.exists': #ako su6testvuva fail ili papka s ime {2}, slaga v {1} True, ina4e slaga False
            var.add(curL[1], os.path.exists(curL[2]))
        elif curL[0] == 'os.path.isfile': #ako su6testvuva fail {2}, slaga v {1} True, ina4e slaga False
            var.add(curL[1], os.path.isfile(curL[2]))
        elif curL[0] == 'os.remove': #istriva fail s ime {1}
            os.remove(curL[1])
        elif curL[0] == 'os.rmdir': #istriva papka s ime {1} (raboti samo ako direktoriqta e prazna) 
            os.rmdir(curL[1])
        elif curL[0] == 'os.strerror': #slaga v {1} kakvo ozna4ava eror kot {2}
            var.add(curL[1], os.strerror(curL[2]))
        elif curL[0] == 'os.system': #ispulnqva komanda {2} v cmdto, i slaga eror koda v {1}
            var.add(curL[1], os.system(curL[2]))
        elif curL[0] == 'os.walk': #slaga v {1} vsi4ki papki v direktoriq {3}; slaga v {2} vsi4ki failove v direktoriq {3}
            item = [[], [], []]
            for item in os.walk(curL[3]):
                break
            var.add(curL[1], item[1])
            var.add(curL[2], item[2])
        #p
        elif curL[0] == 'print': #ispisva na ekrana {2} i {3}, NE slaga \n za krai na reda (askii koda na \n e 10)
            print(curL[1], end=curL[2])
        elif curL[0] == 'python': #runva {1} se edno si go napisal v pitoneca
            exec(curL[1])
        #q
        #r
        elif curL[0] == 'random.choise': #slaga v {1} randomno isbran element ot {2}
            var.add(curL[1], random.choise(curL[2]))
        elif curL[0] == 'random.randfloat': #slaga v {1} randomno izbrano ne cqlo 4islo ot {2} do {3}
            var.add(curL[1], random.uniform(curL[2], curL[3]))
        elif curL[0] == 'random.randint': #slaga v {1} randomno izbrano cqlo 4islo ot {2} do {3}
            var.add(curL[1], random.randint(curL[2], curL[3]))
        elif curL[0] == 'random.random': #slaga v {1} randomno ne cqlo 4islo ot 0 do 1
            var.add(curL[1], random.random())
        elif curL[0] == 'read': #slaga v {1} informaciqta of faila s ime {2}
            f = open(curL[2], 'rb')
            fCont = f.read()
            f.close()
            var.add(curL[1], fCont)
        #s
        elif curL[0] == 'str': #slaga v {1} {2}, konventirano na tekst
            var.add(curL[1], str(curL[2]))
        elif curL[0] == 'subprocess': #se edno si napisal {2} v cmdto si a {1} e output-a na cmd-to ti
            item = subprocess.check_output(curL[2], shell=True)
            var.add(curL[1], item)
        #t
        elif curL[0] == 'time.sleep': #delayva s {1} sekundi
            time.sleep(curL[1])
        elif curL[0] == 'time.time': #slaga v {1} vremeto v sekundi
            var.add(curL[1], time.time())
        elif curL[0] == 'try': #ekzekutira koda do endtry, ako stane gre6ka q zapisva v {1} i zaebava si4ko do endtry
            toExecute = []
            ifs = 0
            end = executingLine
            item = True
            for line in code[executingLine+1:]:
                if var.value(line.split(';')[0]) == 'try':
                    ifs += 1
                elif var.value(line.split(';')[0]) == 'endtry':
                    if ifs == 0:
                        item = False
                        break
                    ifs -= 1
                toExecute.append(line)
                end += 1
            if item:
                print('ERROR: vi6 si try-ovete')
                print(executingLine)
                raise
            executingLine = end
            try:
                executeCode(toExecute)
                item = None
            except:
                item = sys.exc_info()[0].__name__
            var.add(curL[1], item)
        elif curL[0] == 'type': #zapisva v {1} vida na {2} (int, float, str...)
            taipa = type(curL[2]).__name__
            var.add(curL[1], taipa)
        #u
        #v
        #w
        elif curL[0] == 'write': #zapisva {2} v faila s ime {3}
            f = open(curL[2], 'wb')
            f.write(curL[1])
            f.close()
        #x
        #y
        #z

        else:
            try:
                funcArgs, funcValue = functions.value(curL[0])
            except ValueError:
                print('Error (line %s): nqma takava funkciq: "%s" {\n%s\n}' %(executingLine, curL[0], code[executingLine]))
                raise
            for x in range(len(funcArgs)):
                var.add(funcArgs[x], curL[1+x])
            executeCode(funcValue)
        executingLine += 1

def strToCode(code):
    code = code.replace('\t', '')
    code = code.split('\n')
    for x in range(len(code)-1, -1, -1):
        if '--' in code[x]:
            code[x] = code[x][:code[x].index('--')]
        #if code[x] in (''):
        #    del code[x]
    return code

def executeFile(fileName):
    f = open(fileName, 'r')
    code = f.read()
    f.close()
    code = strToCode(code)
    executeCode(code)

executeFile('config.txt')
#executeFile('mersi.txt')
#while True:
#    executeCode(strToCode(input('>>> ')))
