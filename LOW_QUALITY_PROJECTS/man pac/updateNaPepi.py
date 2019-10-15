import socket
import sys
import os
import time

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
    path = path[:-16]
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

def sendAllFilesInDir(dirName):
    dirName2 = dirName[len(getCurrentPath()):]
    if len(dirName2) > 0:
        dirName2 += '\\'
    for item in getAllFiles(dirName):
        if item in notNeededFiles:
            continue
        send(dirName2 + item)
        time.sleep(0.1)
        send(getFileSize(dirName + '\\' + item))
        time.sleep(0.1)

def send2(text):
    #text = str(text)
    #toWitchUser.send(bytes(text.encode('utf-8')))
    s.send(text)

host = '95.111.26.175'
port = 5000

notNeededFolders = ['__pycache__']
notNeededFiles = ['checkForUpdates.py', 'updaterServer.py', 'updateNaPepi.py']


s = socket.socket()
s.connect((host, port))
print('connected')

send('zaPepiRedo')

naPepiGameVer = recive()
for item in getAllFolders(getCurrentPath()):
    if item in notNeededFolders:
        continue
    send(item)
    time.sleep(0.4)
send('{stop}')
time.sleep(0.4)
sendAllFilesInDir(getCurrentPath())
for item in getAllFolders(getCurrentPath()):
    if item in notNeededFolders:
        continue
    sendAllFilesInDir(getCurrentPath()+item)
time.sleep(0.1)
send('{stop}')
while True:
    data = recive()
    if data == '{stop}':
        break
    f = open(getCurrentPath() + '\\' + data, 'rb')
    print('sending file', data)
    fileCont = f.read(1024)
    while fileCont:
        send2(fileCont)
        fileCont = f.read(1024)
    f.close()
    time.sleep(1)
    send('{stop}')
s.close()
print('done')
