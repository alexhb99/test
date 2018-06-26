"""Battleships is a game for two players. Each player places four ships on a board but does not reveal their
location to their opponent. Each ship occupies one or more adjacent squares either horizontally or vertically.
Each player takes it in turn to pick a grid reference. The player scores a hit if the number matches a space
occupied by a ship, or a miss if it does not. The player to sink all their opponents ships first wins."""

#Create a one player game of battleships against a computer opponent.
#Keep score to tell the player how many hits and misses they have had.

from enum import Enum
from random import randint
import time

#Tile enums   
class BaseTile(Enum):
    SHIP1 = 1
    SHIP2  = 2
    SHIP3  = 3
    SHIP4  = 4
    SHIPHIT1 = 5
    SHIPHIT2 = 6
    SHIPHIT3 = 7
    SHIPHIT4 = 8
    SEA = 9
    SEAHIT = 10

class AttackTile(Enum):
    HIT = 1
    MISS = 2
    OPEN = 3

def ShowInstructions():
    print("\nINSTRUCTIONS:")
    print("Battleships is a game for two players. For this program, there will be one player against a computer.")
    print("Each player places four ships on a board but does not reveal their location to their opponent.")
    print("Each ship occupies one or more adjacent squares either horizontally or vertically.")
    print("In this program, a 'O' represents empty space, water, whereas a number represents one of your ships.")
    print("The number shown is the length of the ship it represents.")
    print("Each player takes it in turn to pick a grid reference.")
    print("The player scores a hit if the number matches a space occupied by a ship, or a miss if it does not.")
    print("An H on your home board represents a grid reference where the computer has hit one of your vessels")
    print("An X on your home board shows where the computer has missed a shot taken at you")
    print("An 'X' on your attacking board represents a hit, whereas an 'O' represents a missed shot.")
    print("The player to sink all their opponents ships first wins.\n")
    print("1 point for a hit")
    print("3 points for a destroy")
    print("END OF INSTRUCTIONS.\n")
    waitForInput = input("Ready to continue?\n>>> ")
    print("")

#Returns each tile type's symbol
def SwitchEnumToSymbol(tile):
    if tile == BaseTile.SEA:
        return 'O'
    elif tile == BaseTile.SEAHIT:
        return 'X'
    elif tile == BaseTile.SHIP1:
        return '1'
    elif tile == BaseTile.SHIP2:
        return '2'
    elif tile == BaseTile.SHIP3:
        return '3'
    elif tile == BaseTile.SHIP4:
        return '4'
    elif tile == BaseTile.SHIPHIT1:
        return 'H'
    elif tile ==BaseTile.SHIPHIT2:
        return 'H'
    elif tile == BaseTile.SHIPHIT3:
        return 'H'
    elif tile == BaseTile.SHIPHIT4:
        return 'H'
    elif tile == AttackTile.HIT:
        return 'X'
    elif tile == AttackTile.MISS:
        return 'O'
    elif tile == AttackTile.OPEN:
        return '?'

#Prints the board on the screen
def PrintBoard(board):
    print("")
    xRowStr = "  "
    seperateStr = "  "
    #Setting up edges of board to show coordintaes for x axis
    for a in range(dimension):
        xRowStr += str(a) + " "
        seperateStr += "- "

    print(xRowStr)    
    print(seperateStr)

    #Filling in board and setting up y coordinate edge
    for y in range(dimension):
        buildStr = str(y) + "|"
        for x in range(dimension):
            buildStr += str(SwitchEnumToSymbol(board[x][y])) + " "
        print(buildStr)

    print("\n")

#Generates computer's positions of its ships   
def GeneratePositions(size):
    #1 is vertical, 0 is horizontal
    direction = randint(0,1)

    coords = []
    coords.append([])
    coords.append([]) 

    #For vertical
    if direction == 1:
        #Generates random starting point
        randY = randint(0, dimension - size - 1)
        randX = randint(0, dimension - 1)
        #Adds extra coordinates the ship will take up
        for y in range(size):
            coords[0].append(randX)
            coords[1].append(y + randY)

    #Does same for horizontal, slightly different
    else:
        randY = randint(0, dimension - 1)
        randX = randint(0, dimension - size - 1)
        for x in range(size):
            coords[0].append(x + randX)
            coords[1].append(randY)
            
    #If any of the coordinates already have a ship on them, restart process again
    for a in range(len(coords[0])):
        if compBaseBoard[coords[0][a]][coords[1][a]] == BaseTile(1) or compBaseBoard[coords[0][a]][coords[1][a]] == BaseTile(2) or compBaseBoard[coords[0][a]][coords[1][a]] == BaseTile(3) or compBaseBoard[coords[0][a]][coords[1][a]] == BaseTile(4):
            GeneratePositions(size)
            return

    #Updating boards
    if direction == 1:
        for y in range(size):
            compBaseBoard[randX][y + randY] = BaseTile(size)
    else:
        for x in range(size):
            compBaseBoard[x + randX][randY] = BaseTile(size)


#To get surrounding tiles when finding smart coordinates if hit
def GetSurroundingTiles(closedSet):
    openSet = []
    openSet.append([])
    openSet.append([])

    for a in range(len(closedSet[0])):
        #Check up
        if CheckBounds(closedSet[0][a], closedSet[1][a] - 1):
            if compAttackBoard[closedSet[0][a]][closedSet[1][a] - 1] == AttackTile.OPEN:
                openSet[0].append(closedSet[0][a])
                openSet[1].append(closedSet[1][a] - 1)

        #Check down
        if CheckBounds(closedSet[0][a], closedSet[1][a] + 1):
            if compAttackBoard[closedSet[0][a]][closedSet[1][a] + 1] == AttackTile.OPEN:
                openSet[0].append(closedSet[0][a])
                openSet[1].append(closedSet[1][a] + 1)

        #Check left
        if CheckBounds(closedSet[0][a] - 1, closedSet[1][a]):
            if compAttackBoard[closedSet[0][a] - 1][closedSet[1][a]] == AttackTile.OPEN:
                openSet[0].append(closedSet[0][a] - 1)
                openSet[1].append(closedSet[1][a])

        #Check right
        if CheckBounds(closedSet[0][a] + 1, closedSet[1][a]):
            if compAttackBoard[closedSet[0][a] + 1][closedSet[1][a]] == AttackTile.OPEN:
                openSet[0].append(closedSet[0][a] + 1)
                openSet[1].append(closedSet[1][a])

    
    return openSet

#Returns true if the x and y are within dimension bounds
def CheckBounds(x, y):
    if x < 0 or y < 0 or x > dimension - 1 or y > dimension - 1:
        return False
    else:
        return True

#Returns true if a direction from a point with a certain length doesn't cross any other ships
def TryDirection(size, direc, x, y):
   
    coords = []
    coords.append([])
    coords.append([])
    #Add up coords
    if direc == "U":
        for a in range(size):
            coords[0].append(x)
            coords[1].append(y - a)
    #Add down coords
    elif direc == "D":
        for a in range(size):
            coords[0].append(x)
            coords[1].append(y + a)
    #Add left coords
    elif direc == "L":
        for a in range(size):
            coords[0].append(x - a)
            coords[1].append(y)
    #Add right coords
    elif direc == "R":
        for a in range(size):
            coords[0].append(x + a)
            coords[1].append(y)

    #Test if coords cross another ship
    try:        
        for b in range(len(coords[0])):
            if playerBaseBoard[coords[0][b]][coords[1][b]] == BaseTile(1) or playerBaseBoard[coords[0][b]][coords[1][b]] == BaseTile(2) or playerBaseBoard[coords[0][b]][coords[1][b]] == BaseTile(3) or playerBaseBoard[coords[0][b]][coords[1][b]] == BaseTile(4):
                return False
    except:
        return False

    return True

#Subroutine handling the player's placement of ships
def PlaceShips():
    print("Your empty home board:")
    PrintBoard(playerBaseBoard)
    print("\nPlace your ships in your area")

    #Placing the first ship (seperate as doesn't have extra length)
    while True:
        print("\nPlace ship 1")
        try:
            inputX = int(input("Give x coordinate:\n>>> "))
            inputY = int(input("Give y coordinate:\n>>> "))
        except:
            print("Those are not coordinates")
            continue

        if CheckBounds(inputX, inputY) == False:
            print("The coordinates are out of bounds")
            continue
        
        playerBaseBoard[inputX][inputY] = BaseTile(1)
        break
    
    print("Updated board:")
    PrintBoard(playerBaseBoard)

    #Loops through for each sized ship above 1
    for a in range(3):
        print("\nPlace ship", str(a + 2))
        dirCont = True
        while dirCont == True:
            #Takes starting coords
            try:
                strtInputX = int(input("Give starting x coordinate:\n>>> "))
                strtInputY = int(input("Give starting y coordinate:\n>>> "))
            except:
                print("Those are not coordinates")
                continue
            
            if CheckBounds(strtInputX, strtInputY) == False:
                print("The coordinates are out of bounds")
                continue


            #Gives the player the direction options (if any) they can go in from their start coords
            mustContinue = False
            canUp = False
            canDown = False
            canLeft = False
            canRight = False
            while True:
                directionStr = "\nPick a direction:\n"
                if strtInputY - a - 1 >= 0 and TryDirection(a + 2, "U", strtInputX, strtInputY):
                    directionStr += "'U' to go up\n"
                    canUp = True
                if strtInputY + a + 2 <= dimension and TryDirection(a + 2, "D", strtInputX, strtInputY):
                    directionStr += "'D' to go down\n"
                    canDown = True
                if strtInputX - a - 1 >= 0 and TryDirection(a + 2, "L", strtInputX, strtInputY):
                    directionStr += "'L' to go left\n"
                    canLeft = True
                if strtInputX + a + 2 <= dimension and TryDirection(a + 2, "R", strtInputX, strtInputY):    
                    directionStr += "'R' to go right\n"
                    canRight = True

                if canUp or canDown or canLeft or canRight:
                    print(directionStr)
                else:
                    print("With these coordinates, you cannot place the ship.\nTry a different set of coordinates.")
                    mustContinue = True
                    break
                    
                dire = input(">>> ")
                #Updates boards dependig on direction choice    
                if dire.upper() == "U" and canUp:
                    for b in range(a + 2):
                        playerBaseBoard[strtInputX][strtInputY - b] = BaseTile(a + 2)
                    dirCont = False
                    break
                    
                elif dire.upper() == "D" and canDown:
                    for b in range(a + 2):
                        playerBaseBoard[strtInputX][strtInputY + b] = BaseTile(a + 2)
                    dirCont = False
                    break

                elif dire.upper() == "L" and canLeft:
                    for b in range(a + 2):
                        playerBaseBoard[strtInputX - b][strtInputY] = BaseTile(a + 2)
                    dirCont = False
                    break

                elif dire.upper() == "R" and canRight:
                    for b in range(a + 2):
                        playerBaseBoard[strtInputX + b][strtInputY] = BaseTile(a + 2)
                    dirCont = False
                    break
                else:
                    print("That was not one of the options")
                    
            if mustContinue == True:
                continue


            
        print("Updated board:")
        PrintBoard(playerBaseBoard)
        print("\n")

dimension = 9

print("WELCOME TO BATTLESHIPS!\n")

#Option to show rules and instructions
instructions = input("Do you want to read the rules for the game? Type Y to read.\n>>> ")
if instructions.upper() == "Y":
    ShowInstructions()

outerLayer = True

#Main program loop
while outerLayer == True:
    #Setting up empty boards
    compBaseBoard = [[BaseTile.SEA for x in range (dimension)] for y in range (dimension)]
    compAttackBoard = [[AttackTile.OPEN for x in range (dimension)] for y in range (dimension)]

    playerBaseBoard = [[BaseTile.SEA for x in range (dimension)] for y in range (dimension)]
    playerAttackBoard = [[AttackTile.OPEN for x in range (dimension)] for y in range (dimension)]

    
    
    maxPoints = 0

    #Destroy lists to keep track of hits on specific ships to know when destroyed
    playerDestroys = []
    compDestroys = []

    playerDestroys.append([])
    playerDestroys.append([])
    compDestroys.append([])
    compDestroys.append([])

    #Generating positins for each ship and setting up max points (so know when game ends) and destroys
    for a in range(1,5):
        GeneratePositions(a)
        maxPoints += a + 3

        playerDestroys[0].append(0)
        playerDestroys[1].append(a)

        compDestroys[0].append(0)
        compDestroys[1].append(a)
    
    print("\n")

    #Player placing ships
    PlaceShips()            

    turn = 0
    playerPoints = 0
    playerHits = 0
    playerMisses = 0
    compPoints = 0

    #For smart coordinate calculating
    randomShot = True
    hits = []
    hits.append([])
    hits.append([])

    gameEnded = False

    innerLayer = True
    #Main turn loop
    while innerLayer == True:
        #ENDING AND RESETTING TURN
        turn += 1

        #For if the game has ended
        if gameEnded == True:
            while True:
                contGame = input("\nDo you want to play another game? Y/N\n>>> ")
                if contGame.upper() == "Y":
                    innerLayer = False
                    break
                elif contGame.upper() == "N":
                    outerLayer = False
                    innerLayer = False
                    break
                else:
                    print("That is not valid input!\n")
        if innerLayer == False:
            continue
        
        #PLAYERS TURN
        print("YOUR TURN\n")
        #Displays turn info
        print("Turn:", turn, "  Player Points:", playerPoints, "    Computer Points:", compPoints)
        print("Hits:", playerHits, "    Misses:", playerMisses)
        
        print("\n")

        #Shows current boards
        print("Your attack board:")
        PrintBoard(playerAttackBoard)
        print("\nYour home board:")
        PrintBoard(playerBaseBoard)

        #Takes a coordinate they want to attack
        while True:
            try:
                shotX = int(input("Enter the x coordinate of your target\n>>> "))
                shotY = int(input("Enter the y coordinate of your target\n>>> "))
            except:
                print("Those are not coordinates!")
                continue

            if CheckBounds(shotX, shotY) == False:
                print("Those coordinates are out of bounds!")
            elif playerAttackBoard[shotX][shotY] != AttackTile.OPEN:
                print("Already shot here!")
            else:
                break

        #If they have missed, hit or destroyed
            #Missed
        if compBaseBoard[shotX][shotY] == BaseTile.SEA:
            print("Miss!")
            playerAttackBoard[shotX][shotY] = AttackTile.MISS
            compBaseBoard[shotX][shotY] = BaseTile.SEAHIT
            playerMisses += 1
        else:
            playerDestroys[0][compBaseBoard[shotX][shotY].value - 1] += 1
            #Destroyed
            if playerDestroys[0][compBaseBoard[shotX][shotY].value - 1] == playerDestroys[1][compBaseBoard[shotX][shotY].value - 1]:
                print("Hit and Destroy!")
                playerPoints += 3
            #Hit
            else:
                print("Hit!")
                playerPoints += 1


            #Updating points and boards    
            playerAttackBoard[shotX][shotY] = AttackTile.HIT            
            compBaseBoard[shotX][shotY] = BaseTile(compBaseBoard[shotX][shotY].value + 4)
            playerHits += 1

        #If they have won
        if playerPoints >= maxPoints:
            print("You have won! Congratulations!\n")
            time.sleep(3)
            gameEnded = True
            continue
            

        time.sleep(0.4)
        print("\n")
        
        #COMPUTERS TURN
        time.sleep(0.5)
        print("COMPUTER'S TURN\n")
        time.sleep(0.5)

        #Random shot
        if randomShot == True:
            while True:
                #Generate random coordinates
                shotX = randint(0, dimension - 1)
                shotY = randint(0, dimension - 1)

                #Generate another set of coords if the tile isn't open for attack
                if compAttackBoard[shotX][shotY] != AttackTile.OPEN:
                    continue

                print("Attacking at: [", shotX, ",", shotY,"]\n")
                time.sleep(0.5)
                
               #If they have missed, hit or destroyed
                    #Missed
                if playerBaseBoard[shotX][shotY] == BaseTile.SEA:
                    print("Miss!")
                    compAttackBoard[shotX][shotY] = AttackTile.MISS
                    playerBaseBoard[shotX][shotY] = BaseTile.SEAHIT

                    break
                else:
                    compDestroys[0][playerBaseBoard[shotX][shotY].value - 1] += 1
                    #Destroyed
                    if compDestroys[0][playerBaseBoard[shotX][shotY].value - 1] == compDestroys[1][playerBaseBoard[shotX][shotY].value - 1]:
                        print("Hit and Destroy!")
                        compPoints += 3
                    #Hit
                    else:
                        print("Hit!")
                        hits[0].append(shotX)
                        hits[1].append(shotY)
                        #On next turn, do a smart shot
                        randomShot = False
                        compPoints += 1

                    #Update boards    
                    compAttackBoard[shotX][shotY] = AttackTile.HIT                    
                    playerBaseBoard[shotX][shotY] = BaseTile(playerBaseBoard[shotX][shotY].value + 4)
                    break

        #Smart shot
        else:
            #Get open set of tiles that it can shoot at surrounding previous hits
            opens = GetSurroundingTiles(hits)
            shotRand = randint(0, len(opens[0]) - 1)
            shotX = opens[0][shotRand]
            shotY = opens[1][shotRand]

            print("Attacking at: [", shotX, ",", shotY,"]")

               #If they have missed, hit or destroyed
                    #Missed            
            if playerBaseBoard[shotX][shotY] == BaseTile.SEA:
                print("Miss!")
                compAttackBoard[shotX][shotY] = AttackTile.MISS
                playerBaseBoard[shotX][shotY] = BaseTile.SEAHIT

            else:
                compDestroys[0][playerBaseBoard[shotX][shotY].value - 1] += 1
                #Destroyed
                if compDestroys[0][playerBaseBoard[shotX][shotY].value - 1] == compDestroys[1][playerBaseBoard[shotX][shotY].value - 1]:
                    print("Hit and Destroy!")
                    #Go back to random shooting
                    hits[0] = []
                    hits[1] = []
                    randomShot = True
                    compPoints += 3
                #Hit
                else:
                    print("Hit!")
                    hits[0].append(shotX)
                    hits[1].append(shotY)
                    compPoints += 1

                #Update boards    
                compAttackBoard[shotX][shotY] = AttackTile.HIT
                playerBaseBoard[shotX][shotY] = BaseTile(playerBaseBoard[shotX][shotY].value + 4)
        
        time.sleep(1.5)

        #If the computer has won
        if compPoints >= maxPoints:
            print("\nThe computer has won! You lose!\n")
            time.sleep(3)
            gameEnded = True
        
        print("\n")
        
print("\nThank you for playing!")
