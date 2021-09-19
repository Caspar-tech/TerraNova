import random
from .models import (
    Main,
    Square
)

def Newgrid(FormInput):
    # This function is called when a button is pressed on the website to make a new grid
    # The function deletes all the existing squares from the database
    # Then it take the given number of rows and columns from the form on the website
    # Then it generates as many new squares as there are Rows * Columns
    # It randomly picks the terraintype from a list of available types
    Square.objects.all().delete()

    Rows = int(FormInput.get("Rows"))
    Columns = int(FormInput.get("Columns"))

    TerrainTypes = ["Grass", "Grass", "Water"]

    for r in range(Rows):
        for c in range(Columns):
            RandomTerrain = random.choice(TerrainTypes)
            Newtile = Square(Number=(r*Columns+c), Row=r, Column=c, Terrain=RandomTerrain)
            Newtile.save()

    Center_square = Square.objects.get(Row=(Rows/2), Column=(Columns/2))
    Center_square.Discovered = True
    Center_square.Terrain = "Grass"
    Center_square.save()

    MainGame = Main.objects.get(Name="Game")
    MainGame.Rows = Rows
    MainGame.Columns = Columns
    MainGame.Food = 100
    MainGame.Year = 0
    MainGame.FoodForGrass = 5
    MainGame.FoodForWater = 1
    MainGame.save()

    ClearInfobox()
    Infobox("A new world has been created")

def Discover(Clicked_square):
    # When a tile is clicked on the grid in the html template
    # this functions checks whether a neighbour is already discovered
    # If this is true it "discovers" the clicked tile and reveals the terrain
    # But first we check if the clicked tile really is undiscovered
    if Square.objects.get(Number=Clicked_square).Discovered == False:

        Neighbour_list = Who_are_my_neighbours(Clicked_square)

        Neighbour_discovered = False
        for i in Neighbour_list:
            if Square.objects.get(Number=i).Discovered == True:
                Neighbour_discovered = True

        if Neighbour_discovered == True:
            # Check if player has enough food to discover
            if Food_check(Main.objects.get(Name="Game").Price_discover_tile):
                Tile = Square.objects.get(Number=Clicked_square)
                Tile.Discovered = True
                Tile.save()
                Infobox("You succesfully discovered a new tile")
            else:
                Infobox("Insufficient food ({0}) to discover this tile".format(Main.objects.get(Name="Game").Price_discover_tile))
        else:
            Infobox("You need to discover an adjacent tile first")
    else:
        Infobox("You already discovered this tile")

def Who_are_my_neighbours(Number):
    # When a tile is clicked on the grid in the html template
    # This function returns a list of the number of the neighbour tiles
    Columns = Main.objects.get(Name="Game").Columns
    Rows = Main.objects.get(Name="Game").Rows
    Column = Square.objects.get(Number=Number).Column
    Row = Square.objects.get(Number=Number).Row

    Highest_number = Columns*Rows

    Neighbour_list = []
    if Row != 0:
        Upper_neighbour = Number - Columns
        Neighbour_list.append(Upper_neighbour)

    if Row != (Rows-1):
        Lower_neighbour = Number + Columns
        Neighbour_list.append(Lower_neighbour)

    if Column != 0:
        Left_neighbour = Number - 1
        Neighbour_list.append(Left_neighbour)

    if Column != (Columns-1):
        Right_neighbour = Number + 1
        Neighbour_list.append(Right_neighbour)

    return Neighbour_list

def Food_check(Price):
    # This function operates the food variable in the game
    # It can be called in any other function when a player wants to buy something
    # It will check whether there is enough food, if so will substract the price from the total amount
    # It will return a True or False to the function that called it.
    MainData = Main.objects.get(Name="Game")

    if MainData.Food < Price:
        return False
    else:
        MainData.Food -= Price
        MainData.save()
        return True

def Infobox(Message):
    # This function operates the infobox with information for the player on the template
    # All messages are stored as a string seperated by "-" in one field in the main database
    # This function turns the string into a list and ammends a given new message
    # Then it checks whether the maximum of 7 messages has been reached
    # Then it returns the list to a string and saves it in the main database
    InfoboxList = (Main.objects.get(Name="Game").Infobox).split("-")
    InfoboxList.insert(0, Message)

    Number_of_messages = len(InfoboxList)
    if Number_of_messages > 7:
        InfoboxList.pop()

    InfoboxString = ""
    for i in InfoboxList:
        if i != "":
            InfoboxString += i + "-"
    InfoboxString = InfoboxString[:-1]

    MainGame = Main.objects.get(Name="Game")
    MainGame.Infobox = InfoboxString
    MainGame.save()

def ClearInfobox():
    MainGame = Main.objects.get(Name="Game")
    MainGame.Infobox = ""
    MainGame.save()

def NextYear():
    MainGame = Main.objects.get(Name="Game")
    if MainGame.StartEvent != True:
        MainGame.Year += 1

        MainGame.EndEvent = False

        NumberOfGrassTiles = len(Square.objects.filter(Discovered=True).filter(Terrain="Grass"))
        NumberOfWaterTiles = len(Square.objects.filter(Discovered=True).filter(Terrain="Water"))

        MainGame.NumberOfGrassTiles = NumberOfGrassTiles
        MainGame.NumberOfWaterTiles = NumberOfWaterTiles

        MainGame.Food += (NumberOfGrassTiles * MainGame.FoodForGrass)
        MainGame.Food += (NumberOfWaterTiles * MainGame.FoodForWater)

        MainGame.save()
    else:
        Infobox("Before starting a new year you must make a choice on the dilemma in the overview")

def StartEvent():
    MainGame = Main.objects.get(Name="Game")
    if (MainGame.Year % 2) == 0:
        MainGame.StartEvent = False
    else:
        MainGame.StartEvent = True

    MainGame.save()

def EndEvent(FormInput):
    MainGame = Main.objects.get(Name="Game")
    if MainGame.StartEvent:
        MainGame.StartEvent = False
        MainGame.EndEvent = True

    print(FormInput.get("EventButton"))

    MainGame.save()

