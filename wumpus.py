from world import *
"""
Agent is placed at a random spot in the grid

The user picks what size the grid and what ratio of pits to place in the grid

Options for grid size are: 4x4 and 8x8

Options for ratio size is: 1/8 and 1/16, both are divisible by 16 (4x4 )and 64(8x8)


Agent aims for lowest number
    0 = never visited
    2 = visited
    7 = adjacent to breeze
    If square is 7 and another breeze is felt adjacent to it, add 2
    Add two if the agent visits again

Moves: up, left, down, right
"""

UNKNOWN = 0
VISITED = 2
ADJACENT_BREEZE = 7
ADJACENT_SMELL = 5

SAFE = 0
NOT_SAFE = 1
UNKNOWN_IF_SAFE = 2
GOAL = 3

def calculateThreat(AIworld, threatList, safeList, agentLocation, adjacentLocation, smellList, breezeList):

    #check if has a breeze and add new threat to threat list
    if (AIworld.indicators[agentLocation] == HAS_BREEZE or AIworld.indicators[agentLocation] == HAS_BREEZE_SMELL):
        if (breezeList.count(agentLocation) == 0):
            breezeList += [agentLocation]
        if (safeList[adjacentLocation] == UNKNOWN_IF_SAFE):
            threatList[adjacentLocation] += ADJACENT_BREEZE
            
    #check if has a smell and add new threat to threat list                  
    if (AIworld.indicators[agentLocation] == HAS_SMELL or AIworld.indicators[agentLocation] == HAS_BREEZE_SMELL):
        #add location to smell list
        if (smellList.count(agentLocation) == 0):
            smellList += [agentLocation]
        if (safeList[adjacentLocation] == UNKNOWN_IF_SAFE):
            threatList[adjacentLocation] += ADJACENT_SMELL
			
    if (AIworld.indicators[agentLocation] == NO_INDICATOR):
        safeList[adjacentLocation] = SAFE
        threatList[adjacentLocation] = 0

   
def wumpusLabel(size, notWumpus, smellList):
    wumpusPossibilities = []
    
    if (len(smellList) > 0):

        smellList.sort()
        
        if(len(smellList)==1):

            # If not on left wall, add location to left of smell to wumpusPossibilities
            if(smellList[0]%size != 0):
                wumpusPossibilities += [smellList[0]-1]

            # If not on right wall
            if(smellList[0]%size != size-1):
                wumpusPossibilities += [smellList[0]+1]

            # If not on top
            if(smellList[0]/size != 0):
                wumpusPossibilities += [smellList[0]-size]

            # If not on bottom
            if(smellList[0]/size != size - 1):
                wumpusPossibilities += [smellList[0]+size]

        if(len(smellList)==2):
            if(smellList[1] == smellList[0] + size - 1):
                wumpusPossibilities += [smellList[0]-1]
                wumpusPossibilities += [smellList[0]+size]

            elif(smellList[1] == smellList[0] + size + 1):
                wumpusPossibilities += [smellList[0]+1]
                wumpusPossibilities += [smellList[0]+size]

            elif(smellList[1] == smellList[0] + (size*2)):
                wumpusPossibilities += [smellList[0]+size]

            elif(smellList[1] == smellList[0] + 2):
                wumpusPossibilities += [smellList[0]+1]
                    
        if(len(smellList)==3):
            if (smellList[0] +2 != smellList[1]):
                if(smellList[0]/size != size - 1):
                    wumpusPossibilities += [smellList[0]+size]
            else:
                if(smellList[0]%size != size - 1):
                    wumpusPossibilities +=[smellList[0]+1]
                    
        if(len(smellList)==4):
            wumpusPossibilities += [smellList[0]+size]

        # Makes a copy of wumpusPossibilities so that the index of each possible location
        # remains constant in the checkList while values are being removed from the possibility list
        checkList = wumpusPossibilities[:]
        for x in checkList:
            if (notWumpus[x]):
                wumpusPossibilities.remove(x)
                    
    if(len(wumpusPossibilities)==1):
        return wumpusPossibilities[0]
    else:
        return -1

def findHoles(size, notHole, breezeList, holeList):
    
    for x in range(len(breezeList)):
        possibleHoles = []
        # If not on left wall, add location to left of breeze to possibleHoles
        if(breezeList[x]%size != 0):
            possibleHoles += [breezeList[x]-1]

        # If not on right wall
        if(breezeList[x]%size != size-1):
            possibleHoles += [breezeList[x]+1]

        # If not on top
        if(breezeList[x]/size != 0):
            possibleHoles += [breezeList[x]-size]

        # If not on bottom
        if(breezeList[x]/size != size - 1):
            possibleHoles += [breezeList[x]+size]

        checkList = possibleHoles[:]
        for y in checkList:
            if (notHole[y]):
                possibleHoles.remove(y)

        if(len(possibleHoles) == 1):
            if(holeList.count(possibleHoles[0]) == 0):
                holeList += [possibleHoles[0]]

def printVisited(AIworld, agentVisited, size, holeList, wumpusLocation):
        
    emptyString = ''  # Creates an empty string
    emptyString += AIworld.drawWorld(1)  # Draws the top line of the grid into the empty string

    # Draws the rest of the grid into the string
    for count in range(size * size):
        
        # Draws each data line with spaces and a vertical line separating each element of the row
        emptyString += VERT_LINE + " "

        if(AIworld.world[count] == AGENT):
            emptyString += AGENT
        elif(wumpusLocation == count):
            emptyString += WUMPUS
        elif(holeList.count(count) > 0):
            emptyString += PIT
        elif(AIworld.world[count] == DEAD):
            emptyString += DEAD
        elif(agentVisited[count]):
            emptyString += " "
        else:
            emptyString += "#"

        emptyString += " "

        # Draws the lines between data rows
        if(count % size == size - 1):
            emptyString += VERT_LINE + "\n"
            if(count/size != size-1):
                # Draws lines in between rows
                emptyString += AIworld.drawWorld(2)
            else:
                # Draws the bottom line
                emptyString += AIworld.drawWorld(3)
    
    print emptyString

# Main program loop
while True:

    while True:

        selection = 0
        
        print "\nHow large would you like the world to be?\n\na) 4x4\n\nb) 8x8\n"
        while(selection != 'a' and selection != 'b' and selection != 'c'):
            selection = raw_input("\nYour Choice(lowercase only): ")

        if (selection == 'a'):
            size = 4
        elif (selection == 'b'):
            size = 8

        selection = 0
        
        print "\nHow much of the grid would you like to be filled with holes?\n\na) 1/8 of the grid\n\nb) 1/16 of the grid"
        while(selection < 'a' or selection > 'f'):
            selection = raw_input("\nYour Choice(lowercase only): ")

        if (selection == 'a'):
            holeRatio = 8
        elif (selection == 'b'):
            holeRatio = 16

        selection = 0

        while True:
            
            AIworld = world(size, holeRatio)
            
            agentLocation = AIworld.world.index(AGENT)
            
            status = 0
                
            #list of the threat level of each square on the grid
            threatList = []
            smellList = []
            breezeList = []
            holeList = []
                

            #Make list of visited or not visited squares, to
            #determine where in the indicators list can be looked at
            safeList = []
            agentVisited = []

            #Fill the visited list with false
            for all in range(size * size):
                safeList += [UNKNOWN_IF_SAFE]
                agentVisited += [False]
                threatList += [UNKNOWN]

            status = ALIVE
            wumpusLocation = -1

            # The main game loop starts here       
  
            while True:

                if(AIworld.world.count(AGENT) > 0):
                    agentLocation = AIworld.world.index(AGENT)

                # label visited list with new location
                if(agentVisited[agentLocation] == False):
                    agentVisited[agentLocation] = True
                    safeList[agentLocation] = SAFE
                    threatList[agentLocation] = 0
                    
     
                    # Calculate the threat level of the squares adjacent to the agent 
                
                    #left wall
                    if(agentLocation%size!=0):
                       calculateThreat(AIworld, threatList, safeList, agentLocation, (agentLocation - 1), smellList, breezeList)
                    #right wall
                    if(agentLocation%size!=(size-1)):
                       calculateThreat(AIworld, threatList, safeList, agentLocation, (agentLocation + 1), smellList, breezeList)
                    #top wall
                    if(agentLocation/size!=0):
                       calculateThreat(AIworld, threatList, safeList, agentLocation, (agentLocation - size), smellList, breezeList)
                    #bottom wall
                    if(agentLocation/size!=(size-1)):
                       calculateThreat(AIworld, threatList, safeList, agentLocation, (agentLocation + size), smellList, breezeList)

                threatList[agentLocation] += VISITED

                notWumpus = []
                notHole = []
                for x in range(size*size):
                    if(safeList[x]==SAFE):
                        notWumpus += [True]
                        notHole += [True]
                    else:
                        notWumpus += [False]
                        notHole += [False]

                for x in holeList:
                    notWumpus[x] = True

                if(wumpusLocation == -1):
                    wumpusLocation = wumpusLabel(size, notWumpus, smellList)

                else:
                    notHole[wumpusLocation] = True

                findHoles(size, notHole, breezeList, holeList)

                for x in holeList:
                    safeList[x] = NOT_SAFE
                
                if(wumpusLocation != -1):
                    if(AIworld.hasGold == False):
                        safeList[wumpusLocation] = NOT_SAFE
                    else:
                        safeList[wumpusLocation] = FOUND_GOLD

                print "\n\n\n"

                printVisited(AIworld, agentVisited, size, holeList, wumpusLocation)
                
                print str(AIworld)


                if(AIworld.hasGold):
                    print "The agent has the gold."
                else:
                    print "The agent doesn't have the gold yet."

                if(wumpusLocation == -1):
                    print "The location of the Wumpus is not yet known."
                else:
                    print "The wumpus is in square " + str(wumpusLocation) + "."

                if(len(holeList) == 0):
                    print "No holes have been found yet."
                    
                elif(len(holeList) == 1):
                    print "The location of 1 hole is known."
                else:
                    print "The locations of " + str(len(holeList)) + " holes are known."

                if(AIworld.indicators[agentLocation] == HAS_BREEZE):
                    print "There is a breeze in this square."

                elif(AIworld.indicators[agentLocation] == HAS_SMELL):
                    print "There is a smell in this square."

                elif(AIworld.indicators[agentLocation] == HAS_BREEZE_SMELL):
                    print "This square has a breeze and a smell."

                else:
                    print "There is nothing interesting in this square."


                # Sets variables the the threat levels of each square adjacent to the agent 
                # Sets the threat to -1 if there is a wall in that direction               

                #left wall
                if(agentLocation%size == 0 or safeList[agentLocation-1] == NOT_SAFE):
                    left = -1
                else:
                    left = threatList[agentLocation-1]
                    
                #right wall
                if(agentLocation%size == (size-1) or safeList[agentLocation+1] == NOT_SAFE):
                    right = -1
                else:
                    right = threatList[agentLocation+1]
                    
                #top wall
                if(agentLocation/size == 0 or safeList[agentLocation-size] == NOT_SAFE):
                    up = -1
                else:
                    up = threatList[agentLocation-size]
                    
                #bottom wall
                if(agentLocation/size == (size-1) or safeList[agentLocation+size] == NOT_SAFE):
                    down = -1
                else:
                    down = threatList[agentLocation+size]


                # eliminates all other possibilities if the goal is adjacent to the agent
                
                #above agent
                if(up != -1 and safeList[agentLocation-size] == GOAL):
                    status = AIworld.moveAgentUp()

                #left of agent
                elif(left != -1 and safeList[agentLocation-1] == GOAL):
                    status = AIworld.moveAgentLeft()

                #right of agent
                elif(right != -1 and safeList[agentLocation+1] == GOAL):
                    status = AIworld.moveAgentRight()

                #below agent
                elif(down != -1 and safeList[agentLocation+size] == GOAL):
                    status = AIworld.moveAgentDown()
                
                    
                # Moves the agent in the direction with the lowest threat 


                if(status == ALIVE):
                    #Move agent up
                    if (up != -1 and (up <= left or left == -1) and (up <= down or down == -1) and (up <= right or right == -1)):
                        status = AIworld.moveAgentUp()
                        
                    #Move agent left
                    elif (left != -1 and (left <= down or down == -1) and (left <= right or right == -1)):
                        status = AIworld.moveAgentLeft()
                        
                    #Move agent down
                    elif (down != -1 and (down <= right or right == -1)):
                        status = AIworld.moveAgentDown()
                        
                    #Move agent right
                    else:
                        status = AIworld.moveAgentRight()


                # Breaks the loop if the game is no longer active

                if(status != ALIVE):

                    # Prints the final world state before exiting the loop
                    print "\n\n\n"

                    printVisited(AIworld, agentVisited, size, holeList, wumpusLocation)
                    
                    print str(AIworld)

                    # If the agent fell into a hole
                    if(status == FELL_IN_HOLE):
                        print "You fell into a hole.\nYou Lose.\n\nPress r to restart.\nPress o to change options.\nPress q to exit."
                        break

                    # If the agent was eaten by the wumpus
                    elif(status == EATEN_BY_WUMPUS):
                        print "You were eaten by the Wumpus.\nYou Lose.\n\nPress r to restart.\nPress o to change options.\nPress q to exit."
                        break

                    # If the agent finds the gold, user wins the game
                    elif(status == FOUND_GOLD):
                        print "You have FOUND THE GOLD.\nYou Win.\n\nPress r to restart.\nPress o to change options.\nPress q to exit."
                        break
                    
            selection = 0
            
            while(selection != 'r' and selection != 'o' and selection != 'q'):
                selection = raw_input("Choice: ")

            if(selection == 'o' or selection == 'q'):
                break
        if(selection == 'o' or selection == 'q'):
            break
                
    if(selection == 'q'):
        break
