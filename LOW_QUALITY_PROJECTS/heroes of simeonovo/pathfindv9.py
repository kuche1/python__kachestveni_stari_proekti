import time
import copy

def doko(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True
    return False

class pathfind():
    stepstodopercycle = None
    def start(self, stepstodopercycle, cyclestodo, startx, starty, endx, endy, enddx, enddy, wallsx, wallsy, wallsdx, wallsdy, speed, playerdx, playerdy):
        self.stepstodopercycle = stepstodopercycle
        self.cyclestodo = cyclestodo
        self.endx = endx
        self.endy = endy
        self.enddx = enddx
        self.enddy = enddy
        self.wallsx = wallsx
        self.wallsy = wallsy
        self.wallsdx = wallsdx
        self.wallsdy = wallsdy
        self.speed = speed
        self.playerdx = playerdx
        self.playerdy = playerdy
        
        self.explored = []
        self.explorednum = []
        self.notexplored = [(startx,starty)]
        self.notexplorednum = [0]
    def step(self):
        stepsletftodothiscycle = copy.deepcopy(self.stepstodopercycle)
        while len(self.notexplored) > 0 and stepsletftodothiscycle != 0:
            processnum = 0
            processrast = abs(self.notexplored[0][0]-self.endx) + abs(self.notexplored[0][1]-self.endy)
            for x, item in enumerate(self.notexplored):
                rast = abs(item[0]-self.endx) + abs(item[1]-self.endy)
                if processrast > rast:
                    processnum = x
                    processrast = rast
            #for (x,y) in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
            for (x,y) in ((-1,0),(0,-1),(0,1),(1,0)):
                    pos = [self.notexplored[processnum][0]+x*self.speed,self.notexplored[processnum][1]+y*self.speed]
                    posnum = self.notexplorednum[processnum]
                    if pos not in self.explored:
                        if pos not in self.notexplored:
                            for a, (wx, wy, wdx, wdy) in enumerate(zip(self.wallsx,self.wallsy,self.wallsdx,self.wallsdy)):
                                if doko(pos[0], pos[1], self.playerdx, self.playerdy, wx, wy, wdx, wdy):
                                    break
                            else:
                            #if pos not in walls:          
                                self.notexplored.append(pos)
                                self.notexplorednum.append(posnum+1)
            self.explored.append(self.notexplored[processnum])
            self.explorednum.append(self.notexplorednum[processnum])
            del self.notexplored[processnum]
            del self.notexplorednum[processnum]
            
            if doko(self.explored[-1][0], self.explored[-1][1], self.playerdx, self.playerdy, self.endx, self.endy, self.enddx, self.enddy):
                return True
            #time.sleep(delay)
            stepsletftodothiscycle -= 1
        self.cyclestodo -= 1
        if self.cyclestodo == 0 or len(self.notexplored) > 0:
            return True
    def end(self):
        path = [self.explored[-1]]
        needed = self.explorednum[-1]-1
        while needed != -1:
            index = self.explorednum.index(needed)
            #print(explored[index])
            if abs(self.explored[index][0] - path[-1][0]) <= self.speed and abs(self.explored[index][1] - path[-1][1]) <= self.speed:
                path.append(self.explored[index])
                needed -= 1
            else:
                del self.explored[index]
                del self.explorednum[index]

        return path



