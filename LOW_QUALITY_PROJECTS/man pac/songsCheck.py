import os
import socket
import sys
import songsData
import gameVersion

def sendData(text):
    text = str(text)
    s.send(bytes(text.encode('utf-8')))

def reciveData():
    data = s.recv(1024)
    data = data.decode('utf-8')
    return data

def getCurrentPath():
    path = sys.argv[0]
    path = path[:-13]
    return path

def getAllFilesInDirectory(folderName=None):
    path = getCurrentPath()
    if folderName != None:
        path = path + folderName
    onlyFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyFiles

def getAllFoldersInDirectory(path):
    return [os.path.join(path,o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]

def getFileSize(path, fileName):
    return os.path.getsize(path + fileName)

host = 'localhost'
port = 5000

s = socket.socket()



onlyFiles = getAllFilesInDirectory('myzik')

done = False
while not done:
    done = True
    for x in range(len(onlyFiles)-1, -1, -1):
        for y in range(len(songsData.songs)):
            if onlyFiles[x] == songsData.songs[y]:
                done = False
                del onlyFiles[x]
                del songsData.songs[y]
                break
while True:
    print('=======================')
    print('%s songs missing' %(len(songsData.songs)))
    print('%s additional songs' %(len(onlyFiles)))
    print()
    print('1/missing songs detail')
    print('2/additional songs detail')
    choise = input('>')
    if choise == '1':
        for item in songsData.songs:
            print(item)
        input('PRESS ENTER')
    elif choise == '2':
        for item in onlyFiles:
            print(item)
        input('PRESS ENTER')  
    elif choise == 'rewriteSongs':
        onlyFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        f = open('songsData.py', 'w')
        f.write('songs = %s' %(onlyFiles))
        f.close()
        input('saved')
        quit()
    else:
        print('unknown choise:', choise)
        input('PRESS ENTER')
