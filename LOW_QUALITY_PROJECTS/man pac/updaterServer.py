import socket
import sys
import os
import time
import gameVersion
from threading import Thread

def getCurrentPath():
    path = sys.argv[0]
    path = path[:-16]
    return path

def getAllFolders(path):
    allFolders = [os.path.join(path,o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]
    for x in range(len(allFolders)):
        allFolders[x] = allFolders[x][len(getCurrentPath()):]
    return allFolders


def getAllFiles(path):
    onlyFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyFiles

def getFileSize(path):
    return os.path.getsize(path)

def send(text, toWitchUser):
    text = str(text)
    print("sending: %s" %(text))
    toWitchUser.send(bytes(text.encode('utf-8')))

def send2(text, toWitchUser):
    #text = str(text)
    #toWitchUser.send(bytes(text.encode('utf-8')))
    toWitchUser.send(text)

def recive(witchUser):
    data = witchUser.recv(1024)
    data = data.decode('utf-8')
    print('recived: %s' %(data))
    return data

def recive2(witchUser):
    data = witchUser.recv(1024)
    return data

def sendAllFilesInDir(dirName, c):
    dirName2 = dirName[len(getCurrentPath()):]
    if len(dirName2) > 0:
        dirName2 += '\\'
    for item in getAllFiles(dirName):
        if item in notNeededFiles:
            continue
        send(dirName2 + item, c)
        time.sleep(0.4)
        send(getFileSize(dirName + '\\' + item), c)
        time.sleep(0.4)

def songUpdater():
    global someoneConnecting
    path = getCurrentPath()
    s.listen(1)
    c, addr = s.accept()
    someoneConnecting.append(True)
    print('connection from:' + str(addr))
    send(gameVersion.gameVersion, c)
    data = recive(c)
    if data == 'disconnect':
        c.close()
    elif data == 'connect':
        for item in getAllFolders(getCurrentPath()):
            if item in notNeededFolders:
                continue
            send(item, c)
            time.sleep(0.4)
        send('{stop}', c)
        time.sleep(0.4)
        sendAllFilesInDir(getCurrentPath(), c)
        for item in getAllFolders(getCurrentPath()):
            if item in notNeededFolders:
                continue
            sendAllFilesInDir(getCurrentPath()+item, c)
        time.sleep(0.4)
        send('{stop}', c)
        while True:
            data = recive(c)
            if data == '{stop}':
                break
            f = open(data, 'rb')
            fileCont = f.read(1024)
            while fileCont:
                send2(fileCont, c)
                fileCont = f.read(1024)
            f.close()
            time.sleep(0.4)
            send('{stop}', c)
        c.close()
    elif data == 'zaPepiRedo':
        while True:
            data = recive(c)
            if data == '{stop}':
                break
            if not os.path.exists(getCurrentPath() + '\\' + data):
                os.makedirs(getCurrentPath() + '\\' + data)
        allFiles = []
        while True:
            data = recive(c)
            if data == '{stop}':
                break
            allFiles.append([data])
            data = recive(c)
            allFiles[len(allFiles)-1].append(data)
        brokenFiles = []
        for x in range(len(allFiles)):
            try:
                if int(getFileSize(getCurrentPath() + allFiles[x][0])) != int(allFiles[x][1]):
                    brokenFiles.append(allFiles[x][0])
            except FileNotFoundError:
                brokenFiles.append(allFiles[x][0])
        for x in range(len(brokenFiles)):
            send(brokenFiles[x], c)
            f = open(getCurrentPath() + '\\' + brokenFiles[x], 'wb')
            while True:
                data = recive2(c)
                try:
                    if data.decode('utf-8') == '{stop}':
                        break
                except UnicodeDecodeError:
                    pass
                f.write(data)
            f.close()
        send('{stop}', c)
        c.close()
    else:
        print('unknown command:', data)
        s.close()


host = '95.111.26.175'
port = 5000

s = socket.socket()
s.bind((host, port))

c = list()
addr = list()

someoneConnecting = [True]

notNeededFolders = ['__pycache__']
notNeededFiles = ['checkForUpdates.py', 'updaterServer.py', 'updateNaPepi.py']

while True:
    if len(someoneConnecting) > 0:
        Thread(target=songUpdater).start()
        del someoneConnecting[0]
    #songUpdater()
