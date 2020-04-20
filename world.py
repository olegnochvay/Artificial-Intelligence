import random

WUMPUS = 'W'
AGENT = 'A'
PIT = 'P'
EMPTY = ' '
DEAD = 'X'
GOLD = 'G'
AGENTWON = '@'

NO_INDICATOR = 0 #NO PITS, OR WUMPUS NEARBY
HAS_BREEZE = 1 # PIT NEARBY
HAS_SMELL = 2 # WUMPUS NEARBY
HAS_BREEZE_SMELL = 3 #WUMPUS AND A PIT NEARBY


ALIVE = 0
FELL_IN_HOLE = 1
EATEN_BY_WUMPUS = 2
FOUND_GOLD = 3

HOR_LINE = '-' 
VERT_LINE = '|'
BL_CORNER = '+'
BR_CORNER = '+'
BOT_INT = '+'
TL_CORNER = '+'
TR_CORNER = '+'
TOP_INT = '+'
LEFT_INT = '+'
RIGHT_INT = '+'
MID_INT = '+'


class world:

    def __init__(self, size, holeRatio):
        self.hasGold = False
        random.seed(None)
        self.size = size  # The size of the world, a size of 4 means a 4x4 grid
        self.holeRatio = holeRatio # The number of holes in the world, 4 means that 1/4 of the world
                                   # is filled with holes, 5 means 1/5 and so on
        valid = False

        while(valid == False):

            # Randomly populates the world
            self.world = self.generateWorld()

            # Keeps track of the visited squares for the recursive function
            visited = []

            # Uses the recursive function self.searchGrid to decide
            # if the agent can reach the gold.
            if (self.searchGrid(self.world.index(AGENT), GOLD, visited)):
                visited = []
                valid = self.searchGrid(self.world.index(GOLD), WUMPUS, visited)

        self.indicators = []
        for x in range(self.size*self.size):
            self.indicators += [NO_INDICATOR]
            
        self.generateIndicators()
        
    def __str__(self):
        
        emptyString = ''  # Creates an empty string
        emptyString += self.drawWorld(1)  # Draws the top line of the grid into the empty string

        # Draws the rest of the grid into the string
        for count in range(self.size * self.size):
            
            # Draws each data line with spaces and a vertical line
            # separating each element of the row
            emptyString += VERT_LINE + " " + str(self.world[count]) + " "

            # Draws the lines between data rows
            if(count % self.size == self.size - 1):
                emptyString += VERT_LINE + "\n"
                if(count/self.size != self.size-1):
                    # Draws lines in between rows
                    emptyString += self.drawWorld(2)
                else:
                    # Draws the bottom line
                    emptyString += self.drawWorld(3)
        
        return emptyString

    def drawWorld(self,location):
        
        emptyString = ''
        
        # Draws the top line
        if(location == 1):
            emptyString += TL_CORNER + HOR_LINE*3
            for x in range(1,self.size):
                emptyString += TOP_INT + HOR_LINE*3
            emptyString += TR_CORNER + "\n"

        # Draws the lines in between rows
        elif(location == 2):
            emptyString += LEFT_INT + HOR_LINE*3
            for x in range(1,self.size):
                emptyString += MID_INT + HOR_LINE*3
            emptyString += RIGHT_INT + "\n"

        # Draws the bottom line
        elif(location == 3):
            emptyString += BL_CORNER + HOR_LINE*3
            for x in range(1,self.size):
                emptyString += BOT_INT + HOR_LINE*3
            emptyString += BR_CORNER + "\n"
            
        return emptyString


    # generateWorld                            

    def generateWorld(self):
        
        newWorld = []
        
        #Fill the world with blank tiles
        for x in range(self.size * self.size):
            newWorld += [EMPTY]
            
        #Fill the world with holes
        for x in range(self.size * self.size / self.holeRatio):
            self.placeChar(PIT,newWorld)
            
        #Place a wumpus in the world
        self.placeChar(WUMPUS,newWorld)
        
        #Place a AGENT in the world
        self.placeChar(AGENT,newWorld)

        #Place a GOLD in the world
        self.placeChar(GOLD, newWorld)
        
        return newWorld

    # adjacent To                             

    def adjacentTo(self, x, char):
        if(x/self.size != 0):
            if(self.world[x-self.size] == char):
                return True
            
        if(x/self.size != self.size - 1):
            if(self.world[x+self.size] == char):
                return True
            
        if(x%self.size != 0):
            if(self.world[x-1] == char):
                return True
            
        if(x%self.size != self.size - 1):
            if(self.world[x+1] == char):
                return True
            
        return False


    # generateIndicators                         

    def generateIndicators(self):
        for x in range(self.size*self.size):
            # Adds the value of HAS_BREEZE to all squares that are adjacent to holes
            if(self.adjacentTo(x, PIT)):
                self.indicators[x] += HAS_BREEZE
            # Adds the value of HAS_SMELL to all squares that are adjacent to the wumpus
            if(self.adjacentTo(x, WUMPUS)):
                self.indicators[x] += HAS_SMELL
        

    # searchGrid                             

    def searchGrid(self, x, item, visited):
        
        visited += [x]
        
        #Look at square above
        if(x/self.size != 0 and visited.count(x-self.size) == 0):
            if(self.world[x-self.size] == item):
                return True
            elif(self.world[x-self.size] != PIT and self.world[x-self.size] != WUMPUS):
                if(self.searchGrid(x-self.size, item, visited)):
                    return True
                
        #Look at square below
        if(x/self.size != self.size-1 and visited.count(x+self.size) == 0):
            if(self.world[x+self.size] == item):
                return True
            elif(self.world[x+self.size] != PIT and self.world[x+self.size] != WUMPUS):
                if(self.searchGrid(x+self.size, item, visited)):
                    return True
                
        #Look at square to the left
        if(x%self.size != 0 and visited.count(x-1) == 0):
            if(self.world[x-1] == item):
                return True
            elif(self.world[x-1] != PIT and self.world[x-1] != WUMPUS):
                if(self.searchGrid(x-1, item, visited)):
                   return True
                
        #Look at square to the right
        if(x%self.size != self.size-1 and visited.count(x+1) == 0):
            if(self.world[x+1] == item):
                return True
            elif(self.world[x+1] != PIT and self.world[x+1] != WUMPUS):
                if(self.searchGrid(x+1, item, visited)):
                    return True
                
        return False
    
    # placeChar                               

    def placeChar(self, char, World):
        
        # Generates random numbers until one is found such that world[rand]
        # is an empty space, then places the character in world[rand]
        while True:
            rand = random.randrange(self.size*self.size)
            if (World[rand] == EMPTY):
                World[rand] = char
                break


    # moveAgentUp   
    
    def moveAgentUp(self):
        x = self.world.index(AGENT)
        if(x/self.size != 0):
            return self.moveAgent(x-self.size);
        return ALIVE
        

    # moveAgentDown                            

    def moveAgentDown(self):
        x = self.world.index(AGENT)
        if(x/self.size != self.size - 1):
            return self.moveAgent(x+self.size);
        return ALIVE

    # moveAgentLeft     
    
    def moveAgentLeft(self):
        x = self.world.index(AGENT)
        if(x%self.size != 0):
            return self.moveAgent(x-1);
        return ALIVE


    # moveAgentRight        

    def moveAgentRight(self):
        x = self.world.index(AGENT)
        if(x%self.size != self.size - 1):
            return self.moveAgent(x+1);
        return ALIVE

    # moveAgent                            

    def moveAgent(self, destination):
        # Finds the location of the agent
        x = self.world.index(AGENT)
        
        # Finds the contents of the square above the agent
        contents = self.world[destination]

        # Moves the agent up if the space is empty and a 0 is returned
        if (contents == EMPTY):
            self.world[destination] = AGENT
            self.world[x] = EMPTY
            return ALIVE

        # If there is a pit, the agent falls in and FELL_IN_HOLE is returned
        elif (contents == PIT):
            self.world[destination] = DEAD
            self.world[x] = EMPTY
            return FELL_IN_HOLE

        # If there is a wumpus, the agent falls in and EATEN_BY_WUMPUS is returned
        elif (contents == WUMPUS):
            self.world[destination] = DEAD
            self.world[x] = EMPTY
            return EATEN_BY_WUMPUS

        # If agent finds gold, the agent wins and FOUND_GOLD is returned
        elif (contents == GOLD):
            self.world[destination] = AGENTWON
            self.world[x] = EMPTY
            return FOUND_GOLD

            
        # Otherwise nothing happens and a 0 is returned
        return ALIVE
