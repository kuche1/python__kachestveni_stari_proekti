import socket
import os
import sys
import gameVersion

def send(text):
    text = str(text)
    s.send(bytes(text.encode('utf-8')))

def recive():
    data = s.recv(1024)
    data = data.decode('utf-8')
    return data

def recive2():
    data = s.recv(1024)
    return data

def getCurrentPath():
    path = sys.argv[0]
    path = path[:-18]
    return path

def getAllFiles(path):
    onlyFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyFiles

def getAllFolders(path):
    allFolders = [os.path.join(path,o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]
    for x in range(len(allFolders)):
        allFolders[x] = allFolders[x][len(getCurrentPath()):]
    return allFolders

def getFileSize(path):
    return os.path.getsize(path)

host = '95.111.26.175'
port = 5000

s = socket.socket()
print('connecting to server')
s.connect((host, port))
print('connected to server')
print('getting latest game version')
data = recive()
if float(data) == float(gameVersion.gameVersion)+1:
    send('disconnect')
    s.close()
    print('you have the latest game version')
    input('PRESS ENTER')
    quit()
else:
    print('there is an update to the game')
    choise = input('would you like to download it?(y/n)')
    if choise == 'n':
        send('disconnect')
        s.close()
        print('PRESS ENTER')
        quit()
    elif choise == 'y':
        send('connect')
        print('reciving game directories')
        while True:
            data = recive()
            if data == '{stop}':
                break
            if not os.path.exists(getCurrentPath() + '\\' + data):
                os.makedirs(getCurrentPath() + '\\' + data)
        allFiles = []
        while True:
            data = recive()
            if data == '{stop}':
                break
            allFiles.append([data])
            data = recive()
            allFiles[len(allFiles)-1].append(data)
        print('checking for broken files')
        brokenFiles = []
        for x in range(len(allFiles)):
            try:
                if int(getFileSize(getCurrentPath() + allFiles[x][0])) != int(allFiles[x][1]):
                    brokenFiles.append(allFiles[x][0])
            except FileNotFoundError:
                brokenFiles.append(allFiles[x][0])
        print('%s broken files' %(len(brokenFiles)))
        #print(brokenFiles)
        for x in range(len(brokenFiles)):
            send(brokenFiles[x])
            f = open(getCurrentPath() + '\\' + brokenFiles[x], 'wb')
            while True:
                data = recive2()
                try:
                    if data.decode('utf-8') == '{stop}':
                        break
                except UnicodeDecodeError:
                    pass
                f.write(data)
            f.close()
            print('%s/%s done' %(x+1, len(brokenFiles)))
        send('{stop}')
        s.close()
        print('all game files updated')
        input('PRESS ENTER')


            
