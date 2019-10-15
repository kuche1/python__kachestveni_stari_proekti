#playerIP = '94.236.254.251'#'95.111.26.175'#'95.111.26.175'#'130.204.155.167'#'130.204.166.86'
displayX = 1000
displayY = 1000
displayR = 480
fullScreen = False
font = 'Candara.ttf'

f = open('FPS.txt', 'r')
FPS = int(f.read())
f.close()

f = open('playerIP.txt', 'r')
playerIP = f.read()
f.close()
