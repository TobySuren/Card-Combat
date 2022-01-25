#Libraries used:
from random import randint #used for picking random numbers for generating cards
from time import sleep #used to add delay to increase tension when playing


#Card list:
#1-9 in red, yellow and blue
#K in white
#round counter in white
#0 in white

#Priority:
#Highest card always wins (W in white beats all), if cards are the same number:
#Red beats yellow
#Yellow beats blue
#Blue beats red
#White beats other colours


#Functions:

def clearScreen(): #creates a lot of empty lines to somewhat clear the screen
    print(80 * "\n")


def validStrInput(inputQuestion = "", subsequentInputQuestions = "", failedWarningName = "input", clearScreenAfterInput = False): #used to check if an input can be written to a file
    string = input(inputQuestion)
    allowed = False
    testFile = open("validWriteTester.txt", "w")
    while not allowed:
        try:
            testFile.write(string)
            allowed = True
        except:
            if clearScreenAfterInput:
                clearScreen()
            print("This "+failedWarningName+" contains forbidden characters.")
            string = input(subsequentInputQuestions)
            
    testFile.close()
    testFile = open("validWriteTester.txt", "w")
    testFile.write("< DATA IN BETA STATE. FOR ANY QUALITY CONCERNS PLEASE CONTACT KAMINSKI DATA STORAGE MFG. >")
    testFile.close()
    return string

def encrypt(string): #encrypts a string using a custom irreversible cipher to be saved as a password
    encryptedString = ""
    for i in range(len(string)):
        character = string[i]
        characterId = ord(character)
        encryptedId = ((len(string) + i) * characterId) % 93 + 33
        encrypted = chr(encryptedId)
        encryptedString += encrypted
        
        addChar = characterId % 2 > 0
        if addChar:
            addedEncryptedId = ((len(string) * i) * characterId) % 93 + 33
            addedEncrypted = chr(addedEncryptedId)
            encryptedString += addedEncrypted
            
    return encryptedString


def shuffleCards(): #shuffles the cards into a random order
    cardsAvailable = [] #an empty list for the unshuffled cards
    shuffledDeck = [] #an empty list for the unshuffled cards
    
    for i in range(1, 10): #adds a card for every number and colour
        for i2 in range(3):
            cardsAvailable.append(str(i) + str(i2))

    cardsAvailable.append("K") #adds the 3 special cards
    cardsAvailable.append("R")
    cardsAvailable.append("03") 

    for i in range(29): #adds each card to the shuffled deck in a random order, similarly to insertion sort
        cardPosition = randint(1, (29 - i))
        shuffledDeck.append(cardsAvailable[cardPosition])
        cardsAvailable.pop(cardPosition)

    shuffledDeck.append(cardsAvailable[0])
    
    return shuffledDeck


def displayCards(cardCount = 1, shownCardStat = False, shownCardPosition = False): #creates ASCII art for a list of cards, having one card reveal its stats if specified
    print(cardCount * "+-----+  ") #displays the top layer of the card

    if not (shownCardStat == "" or shownCardPosition): #displays the middle part of unrevealed cards
        for i in range(2):
            print(cardCount * "|     |  ")
        print(cardCount * "|  ?  |  ")
        for i in range(2):
            print(cardCount * "|     |  ")

    elif shownCardStat and shownCardPosition: #displays the middle part of revealed and unrevealed cards
        cardsBeforeShown = shownCardPosition - 1 #how many cards are to the left of the revealed card
        cardsAfterShown = cardCount - shownCardPosition #how many cards are to the right of the revealed card

        cardNumber = "0" #the number shown on the card
        cardColour = "W" #the colour shown on the card
        numbersToColours = ["R","Y","B","W"] #an array used to convert numbers to colours
        
        if shownCardStat == "K": #picks card values depending on card type
            cardNumber = "K"
            cardColour = "W"

        elif shownCardStat == "R":
            cardNumber = "Ω"
            cardColour = "W"

        else:
            cardNumber = shownCardStat[0]
            cardColour = numbersToColours[int(shownCardStat[1])]

        #displays the cards' middles, including the revealed card
        print(cardsBeforeShown * "|     |  " + ("|" + cardColour + "    |  ") + cardsAfterShown * "|     |  ")
        print(cardCount * "|     |  ")
        print(cardsBeforeShown * "|  ?  |  " + ("|  " + cardNumber + "  |  ") + cardsAfterShown * "|  ?  |  ")
        print(cardCount * "|     |  ")
        print(cardsBeforeShown * "|     |  " + ("|    " + cardColour + "|  ") + cardsAfterShown * "|     |  ")

                 
    else: #errors if inputted incorrectly
        print("Error: shownCardStat or shownCardPosition missing")

    print(cardCount * "+-----+  ") #displays the bottom layer of the card
    

def main():
    clearScreen()
    usersFileLines = [] #the lines for the users file
    try: #makes sure a usernames file exists
        file = open("users.txt", "r")
        usersFileLines = file.readlines()
        file.close()

        if len(usersFileLines) % 2 != 0 or (len(usersFileLines) != 0 and (usersFileLines[-1])[-1:] != "\n"): #checks if the file is not in the correct format
            print("File users.txt has been corrupted. Clearing the file.\n")
            file = open("users.txt", "w")
            usersFileLines = []
            file.close()
            
    except:
        print("File users.txt could not be found. A new users.txt has been created.\n")
        file = open("users.txt", "w")
        file.close()

    try: #makes sure a highscores file exists
        file = open("highscores.txt", "r")
        highscoresFileLines = file.readlines()
        file.close()

        if len(highscoresFileLines) % 2 != 0 or len(highscoresFileLines) != 10 or (highscoresFileLines[-1])[-1:] != "\n": #checks if the file is not in the correct format
            print("File highscores.txt has been corrupted. Clearing the file.\n")
            file = open("highscores.txt", "w")
            for i in range(5):
                file.write("Empty\n0\n")
            file.close()
        else:
            for i in range(1, 10, 2): #makes sure that each score is an actual integer
                try:
                    int(highscoresFileLines[i])
                except:
                    print("File highscores.txt has been corrupted. Clearing the file.\n")
                    file = open("highscores.txt", "w")
                    for i2 in range(5):
                        file.write("Empty\n0\n")
                    file.close()
                    break
        
    except:
        print("File highscores.txt could not be found. A new highscores.txt has been created.\n")
        file = open("highscores.txt", "w")
        for i in range(5):
            file.write("Empty\n0\n")
        file.close()

    player1User = ""
    if len(usersFileLines) > 0: #logs in or creates player 1
        print("Welcome Player 1. Would you like to:")
        print("a. Log in")
        print("b. Create a new user")

        loop = True #repeats until a correct option is entered
        choice = ""
        while loop:
            choice = input("Please type a or b:\n")
            if len(choice) == 1:
                if choice == "a":
                    loop = False
                    userNotFound = True
                    while userNotFound: #uses linear search to find the username then checks password
                        username = input("\nPlease enter your username:\n")
                        password = input("Please enter your password:\n")
                        clearScreen()
                        for i in range(0, len(usersFileLines), 2):
                            if (usersFileLines[i])[:-1] == username and (usersFileLines[i+1])[:-1] == encrypt(password):
                                print("Username and password correct!\n")
                                userNotFound = False
                                player1User = username
                                
                        if userNotFound:
                            print("Username or password incorrect!")
                        
                elif choice == "b": #creates a new user
                    loop = False
                    usersFile = open("users.txt", "a")
                    player1User = validStrInput("\nPlease enter a username to begin creating a new user:\n", "Please enter a different username:\n", "username", False)
                    noNewUser = True #checks if the new username exists
                    while noNewUser:
                        noNewUser = False
                        for i in range(0, len(usersFileLines), 2):
                            if player1User+"\n" == usersFileLines[i]:
                                noNewUser = True
                                player1User = validStrInput("This username already exists.\nPlease enter a different username:\n", "Please enter a different username:\n", "username", False)
                            
                    
                    usersFile.write(player1User+"\n")
                    usersFile.write(encrypt(validStrInput("Please enter a password:\n", "Please enter a different password:\n", "password", True))+"\n")
                    clearScreen()
                    print("New user created!\n")
                    usersFile.close()
                    
                else:
                    print("That is not an option.")
            else:
                print("Please enter your choice as a single letter.")
        
    else: #creates a new user if there is none
        usersFile = open("users.txt", "w")
        player1User = validStrInput("Welcome Player 1.\nNo users detected. Please enter a username to begin creating a new user:\n", "Please enter a different username:\n", "username", False)
        usersFile.write(player1User+"\n")
        usersFile.write(encrypt(validStrInput("Please enter a password:\n", "Please enter a different password:\n", "password", True))+"\n")
        clearScreen()
        usersFile.close()

    player2User = ""
    if len(usersFileLines) > 2: #logs in or creates player 2
        print("Welcome Player 2. Would you like to:")
        print("a. Log in")
        print("b. Create a new user")

        loop = True #repeats until a correct option is entered
        choice = ""
        while loop:
            choice = input("Please type a or b:\n")
            if len(choice) == 1:
                if choice == "a":
                    loop = False
                    userNotFound = True
                    while userNotFound: #uses linear search to find the username then checks password
                        username = input("\nPlease enter your username:\n")
                        password = input("Please enter your password:\n")
                        clearScreen()
                        if username == player1User:
                            print("Player 1 has already logged in with this user! Please pick a different user.")

                        else:
                            for i in range(0, len(usersFileLines), 2):
                                if (usersFileLines[i])[:-1] == username and (usersFileLines[i+1])[:-1] == encrypt(password):
                                    print("Username and password correct!\n")
                                    userNotFound = False
                                    player2User = username
                                
                            if userNotFound:
                                print("Username or password incorrect!")
                        
                elif choice == "b": #creates a new user
                    loop = False
                    usersFile = open("users.txt", "a")
                    player2User = validStrInput("\nPlease enter a username to begin creating a new user:\n", "Please enter a different username:\n", "username", False)
                    noNewUser = True #checks if the new username exists
                    while noNewUser:
                        noNewUser = False
                        for i in range(0, len(usersFileLines), 2):
                            if player2User+"\n" == usersFileLines[i]:
                                noNewUser = True
                                player2User = validStrInput("This username already exists.\nPlease enter a different username:\n", "Please enter a different username:\n", "username", False)
                            
                    usersFile.write(player2User+"\n")
                    usersFile.write(encrypt(validStrInput("Please enter a password:\n", "Please enter a different password:\n", "password", True))+"\n")
                    clearScreen()
                    print("New user created!\n")
                    usersFile.close()
                    
                else:
                    print("That is not an option.")
            else:
                print("Please enter your choice as a single letter.")

    else: #creates a new user if there is none
        usersFile = open("users.txt", "a")
        player2User = validStrInput("Welcome Player 2.\nNo other users detected. Please enter a username to begin creating a new user:\n", "Please enter a different username:\n", "username", False)
        noNewUser = True #checks if the new username exists
        while noNewUser:
            noNewUser = False
            if player2User == player1User:
                noNewUser = True
                player2User = validStrInput("This username already exists.\nPlease enter a different username:\n", "Please enter a different username:\n", "username", False)
            usersFile.write(player2User+"\n")
        usersFile.write(encrypt(validStrInput("Please enter a password:\n", "Please enter a different password:\n", "password", True))+"\n")
        clearScreen()
        usersFile.close()

    print("Logged in users:")
    print("Player 1: "+player1User)
    print("Player 2: "+player2User)
    input("\nPlease press enter to continue.\n")
    menu(player1User, player2User)


def menu(player1User, player2User):
    clearScreen()
    print("  +-----+")
    print("  |     |")
    print("  |  C a r d")
    print("  |     |")
    print("  |  C o m b a t")
    print("  |     |")
    print("  +-----+")

    print("\nWelcome to Card Combat!")
    print("Options:")
    print("a. Play")
    print("b. Highscores")
    print("c. Help")
    print("d. Quit")
    choice = ""
    loop = True #makes sure the player inputs a valid option
    while loop:
        choice = input("Please enter your choice (a/b/c):\n")
        if len(choice) == 1:
            if choice == "a":
                loop = False

                loop2 = True #makes sure the player inputs a valid number of rounds
                rounds = input("How many cards should each player start with?\n")
                while loop2:
                    if rounds != "":
                        try:
                            rounds = int(rounds)
                            if rounds >= 4 and rounds <= 15:
                                loop2 = False
                                print(rounds)
                                playGame(rounds, player1User, player2User)
                                menu(player1User, player2User)
                            elif rounds <= 3:
                                print("There must be at least 4 cards per player.")
                                rounds = input("How many rounds should be played?\n")
                            else:
                                print("There cannot be more than 15 cards per player.")
                                rounds = input("How many rounds should be played?\n")
                        except:
                            print("That is not a number.")
                            rounds = input("How many cards should each player start with?\n")
                    else:
                        rounds = input("How many cards should each player start with?\n")

            elif choice == "b": #prints the highscore leaderboard in a format
                loop = False
                clearScreen()
                highscoresFile = open("highscores.txt", "r")
                highscoresFileLines = highscoresFile.readlines()
                for i in range(5):
                    if highscoresFileLines[2*i] == "Empty\n":
                        print(str(i+1) + ". No one")
                    else:
                        print(str(i+1) + ". " + (highscoresFileLines[2*i])[:-1] + ": " + (highscoresFileLines[2*i+1])[:-1] )
                input("\nPress enter to return to the main menu.\n")
                menu(player1User, player2User)

            elif choice == "c": #prints info on card values and hierarchy
                loop = False
                clearScreen()
                displayCards(4)
                print("\nAt the start of each game, you will be given some cards each and will be asked to say the position of a card in your deck.")
                input("\nPress enter to continue.\n")

                clearScreen()
                displayCards(4, "40", 1)
                print("\nAfter both players pick their cards, the picked cards will be revealed.")
                print("Each card has a colour value and a number value.")
                print("R = red.")
                print("Y = yellow.")
                print("B = blue.")
                print("W = white.")
                input("\nPress enter to continue.\n")

                clearScreen()
                displayCards(4, "03", 2)
                print("\nIf one card's number is higher than the other, that card always wins.")
                print("If the cards' numbers are the same, the winner depends on colour:")
                print("Red beats yellow.")
                print("Yellow beats blue.")
                print("Blue beats red.")
                print("White beats all other colours.")
                input("\nPress enter to continue.\n")

                clearScreen()
                displayCards(4, "K", 3)
                print("The K card beats all cards no matter what.")
                print("After winning, both teams lose that card and the winner gains a point.")
                print("Depending on how large the difference between the cards' numbers are, the winner recieves a score increase.")
                input("\nPress enter to continue.\n")

                clearScreen()
                displayCards(4, "R", 4)
                print("After winning, the game repeats with one less card, going on to round 2.")
                print("The Ω card has a number equal to the round number when the card is played.")
                print("You keep on playing until each player only has one card left.")
                print("Once this happens, whoever has the most points (or the highest score if points are equal) wins the game.")
                print("Only the winner can have their score added to the leaderboard if their score is high enough.")
                input("\nPress enter to return to the main menu.\n")
                menu(player1User, player2User)
            
            elif choice == "d":
                loop = False
                print("Thank you for playing!")
                
            else:
                print("That is not a valid option.")
        else:
            print("Choices should be written as a single letter.")


def playGame(cardsPerPlayer = 5, player1User = "", player2User = ""): #plays the game itself
    cardsToBeDealed = shuffleCards() #shuffles the deck and sets it to a list
    player1Deck = [] #player 1's deck
    player2Deck = [] #player 2's deck
    
    for i in range(cardsPerPlayer): #takes the first cards from the shuffled deck and gives them to the players
        player1Deck.append(cardsToBeDealed[0])
        cardsToBeDealed.pop(0)

        player2Deck.append(cardsToBeDealed[0])
        cardsToBeDealed.pop(0)

    roundNumber = 1 #used for highscores and the round counter card
    player1Wins = 0 #used to see who wins
    player2Wins = 0
    player1ScoreDif = 0 #used for highscores (how much value won by overall)
    player2ScoreDif = 0

    while len(player1Deck) > 1: #the main round itself, repeating until each player has 1 card
    
        clearScreen() #clears screen then displays each players' decks
        print("Round " + str(roundNumber) + "\n\n"+player1User+" " + player1Wins * "*")
        displayCards(len(player1Deck))
        print("\n\n"+player2User+" " + player2Wins * "*")
        displayCards(len(player2Deck))

        print()
        loop = True #makes sure the player inputs a valid card number
        player1Choice = input(player1User+", please pick a card by entering its number from left to right:\n")
        while loop:
            if player1Choice != "":
                try:
                    player1Choice = int(player1Choice)
                    if player1Choice <= len(player1Deck):
                        loop = False
                    else:
                        print("You do not have " + str(player1Choice) + " cards.")
                        player1Choice = input("Please pick a card by entering its number from left to right:\n")
                except:
                    print("That is not a number.")
                    player1Choice = input("Please pick a card by entering its number from left to right:\n")
            else:
                player1Choice = input("Please pick a card by entering its number from left to right:\n")

        print()
        loop = True #same as above but for player 2
        player2Choice = input(player2User+", please pick a card by entering its number from left to right:\n")
        while loop:
            if player2Choice != "":
                try:
                    player2Choice = int(player2Choice)
                    if player2Choice <= len(player2Deck):
                        loop = False
                    else:
                        print("You do not have " + str(player2Choice) + " cards.")
                        player2Choice = input("Please pick a card by entering its number from left to right:\n")
                except:
                    print("That is not a number.")
                    player2Choice = input("Please pick a card by entering its number from left to right:\n")
            else:
                player2Choice = input("Please pick a card by entering its number from left to right:\n")

        for i in range(3, 0, -1): #creates a 3 2 1 countdown with a 1 second delay between numbers
            clearScreen()
            print(str(i))
            sleep(1)

        player1Card = player1Deck[player1Choice - 1] #player 1's chosen card
        player2Card = player2Deck[player2Choice - 1] #player 2's chosen card
    
        clearScreen() #clears screen then displays each players' decks with their revealed card
        print()
        displayCards(len(player1Deck), player1Card, player1Choice)
        print("\n\n")
        displayCards(len(player2Deck), player2Card, player2Choice)
        print()

        player1Value = 0 #player 1's number
        player2Value = 0 #player 2's number
        player1Colour = "W" #player 1's colour
        player2Colour = "W" #player 2's colour
    
        try: #check if player 1 has a number card and gives the appropriate stats
            player1Value = int(player1Card[0])
            player1Colour = player1Card[1]
        except: #otherwise give special card specific stats
            if player1Card == "K":
                player1Value = 10
                player1Colour = "W"
            else:
                player1Value = roundNumber
                player1Colour = "W"

        try: #check if player 2 has a number card and gives the appropriate stats
            player2Value = int(player2Card[0])
            player2Colour = player2Card[1]
        except: #otherwise give special card specific stats
            if player2Card == "K":
                player2Value = 10
                player2Colour = "W"
            else:
                player2Value = roundNumber
                player2Colour = "W"

        if player1Value == player2Value: #if the players have the same value check who wins by colour
            if player1Colour == "R": 
                if player2Colour == "Y":
                    print(player1User+" wins!")
                    player1Wins += 1
                else:
                    print(player2User+" wins!")
                    player2Wins += 1 
                    
            if player1Colour == "Y":
                if player2Colour == "B":
                    print(player1User+" wins!")
                    player1Wins += 1 
                else: 
                    print(player2User+" wins!")
                    player2Wins += 1 
                    
            if player1Colour == "B": 
                if player2Colour == "R": 
                    print(player1User+" wins!")
                    player1Wins += 1 
                else: 
                    print(player2User+" wins!")
                    player2Wins += 1 
                    
            else: 
                print(player1User+" wins!")
                player1Wins += 1 
            
        elif player1Value > player2Value: #if player 1 has higher
            print(player1User+" wins!")
            player1Wins += 1 
            player1ScoreDif += player1Value - player2Value 

        else: #if player 2 has higher
            print(player2User+" wins!")
            player2Wins += 1 
            player2ScoreDif += player2Value - player1Value 

        input("\nPress enter to continue.\n")
        
        roundNumber += 1 #increments the round counter and removes played cards
        if len(player1Deck) > 0:
            player1Deck.pop(player1Choice - 1) 
            player2Deck.pop(player2Choice - 1) 
    
    clearScreen()
    print("And the winner...") #messages with delay to build suspense
    sleep(1)
    print("...is...")
    sleep(2)

    player1Score = (player1ScoreDif * 100) // roundNumber
    player2Score = (player2ScoreDif * 100) // roundNumber

    winner = ""
    winnerScore = 0
    if player1Wins > player2Wins: #checks who has highest wins and displays message accordingly
        print(player1User+"!")
        winner = player1User
        winnerScore = player1Score
    elif player2Wins > player1Wins:
        print(player2User+"!")
        winner = player2User
        winnerScore = player2Score
    else:
        if player1Score > player2Score: #if wins are equal, check score difference
            print(player1User+"!")
            winner = player1User
            winnerScore = player1Score
        else:
            print(player2User+"!")
            winner = player2User
            winnerScore = player2Score

    sleep(2)
    input("\nPress enter to continue.\n")
    clearScreen()
    print("Scores:")
    print(player1User+"'s wins: "+str(player1Wins)) #displays stats
    print(player1User+"'s score: "+str(player1Score))
    print(player2User+"'s wins: "+str(player2Wins))
    print(player2User+"'s score: "+str(player2Score))

    highscoresFile = open("highscores.txt", "r") #uses a variation of insertion sort to add the highscore to the leaderboard
    highscoresFileLines = highscoresFile.readlines()
    highscoresFile.close()
    if winnerScore > int(highscoresFileLines[9]):
        print(winner+", you got a new highscore!")
        highscoresFile = open("highscores.txt", "w")
        insertedWinner = False
        for i in range(1, 10, 2):
            if winnerScore > int(highscoresFileLines[i]) and not insertedWinner:
                highscoresFile.write(winner+"\n"+str(winnerScore)+"\n")
                insertedWinner = True
                if i < 9:
                    highscoresFile.write(highscoresFileLines[i-1]+highscoresFileLines[i])
            else:
                if i < 9:
                    highscoresFile.write(highscoresFileLines[i-1]+highscoresFileLines[i])
        

    input("\nPress enter to return to the main menu.\n")

    
main()
