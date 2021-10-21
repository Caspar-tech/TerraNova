import random
from .models import (
    Main,
    Square,
    Highscore
)

def Newgrid():
    # This function is called when a button is pressed on the website to make a new grid
    # The function deletes all the existing squares from the database
    # Then it take the given number of rows and columns from the form on the website
    # Then it generates as many new squares as there are Rows * Columns
    # It randomly picks the terraintype from a list of available types
    Square.objects.all().delete()

    Rows = 10
    Columns = 10

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
    MainGame.FoodForGrass = 4
    MainGame.FoodForWater = 7
    MainGame.StartEvent = False
    MainGame.EndEvent = False
    MainGame.Boat = False
    MainGame.GameEnded = False
    MainGame.GameEndedSucces = False
    MainGame.GameEndedHighscore = False
    MainGame.save()

    ClearInfobox()
    Infobox("You discover the world by clicking on a undiscovered (brown) tile on the world map. "
            "When you click on a new tile you will read here whether your discovery was succesfull. "
            "When you are done with discovering click on the Next Year button to proceed to the next year.")

    Infobox("You are the leader of a small tribe. You live from what you collect from the lands you know. "
            "This provides you and your fellow tribesman with the food you need, year in year out. "
            "But great disaster is ahead. The high priest had a vision that great droughts will happen in 10 years. "
            "In order to save your tribe, you must gather as much food as possible. "
            "Discovering new parts of the world will cost food but will also supply you "
            " with more food in the long run. How wise a leader are you?")

def Discover(Clicked_square):
    # When a tile is clicked on the grid in the html template
    # this functions checks whether a neighbour is already discovered
    # If this is true it "discovers" the clicked tile and reveals the terrain

    # But first we check if the tile is water and boating is already discovered and,
    # then we check if the clicked tile really is undiscovered
    MainGame = Main.objects.get(Name="Game")
    if Square.objects.get(Number=Clicked_square).Discovered == False:
        Neighbour_list = Who_are_my_neighbours(Clicked_square)

        Neighbour_discovered = False
        for i in Neighbour_list:
            if Square.objects.get(Number=i).Discovered == True:
                Neighbour_discovered = True

        if Neighbour_discovered == True:
            # Check if player has enough food to discover
            if MainGame.Price_discover_tile <= MainGame.Food:

                Tile = Square.objects.get(Number=Clicked_square)
                if Tile.Terrain == "Grass":
                    Tile.Discovered = True
                    MainGame.Food -= MainGame.Price_discover_tile
                    MainGame.save()
                    Infobox("You succesfully discovered a new tile")

                if Tile.Terrain == "Water":
                    if MainGame.Boat == True:
                        Tile.Discovered = True
                        MainGame.Food -= MainGame.Price_discover_tile
                        MainGame.save()
                        Infobox("You succesfully discovered a new tile")
                    else:
                        Infobox("Such a wet and cold place... I don't want to discover this tile")
                Tile.save()
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

def Infobox(Message):
    # This function operates the infobox with information for the player on the template
    # All messages are stored as a string seperated by "-" in one field in the main database
    # This function turns the string into a list and ammends a given new message
    # Then it checks whether the maximum of 7 messages has been reached
    # Then it returns the list to a string and saves it in the main database
    InfoboxList = (Main.objects.get(Name="Game").Infobox).split("-")
    InfoboxList.insert(0, Message)

    Number_of_messages = len(InfoboxList)
    if Number_of_messages > 20:
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

        MainGame.FoodForGrassCurrentYear = MainGame.FoodForGrass
        MainGame.FoodForWaterCurrentYear = MainGame.FoodForWater

        MainGame.save()
    else:
        Infobox("Before starting a new year you must make a choice on the dilemma in the overview")

def StartEvent():
    MainGame = Main.objects.get(Name="Game")

    if MainGame.Year == 2:
        MainGame.TextEvent = "These berries look delicious!"
        MainGame.EventButton1 = "Eat them"
        MainGame.EventButton2 = "Probably also poisonous"
        MainGame.StartEvent = True
    elif MainGame.Year == 4:
        MainGame.TextEvent = "A man on a wooden floating device comes your way over an undiscovered tile. He offers you his knowledge of this so called 'ship'"
        MainGame.EventButton1 = "Please, explain"
        MainGame.EventButton2 = "No, sounds like witchcraft!"
        MainGame.StartEvent = True
    elif MainGame.Year == 6:
        MainGame.GameEnded = True
        if MainGame.Food > 100:
            MainGame.GameEndedSucces = True
            MainGame.GameEndedHighscore = True

    MainGame.save()

def EndEvent(FormInput):
    MainGame = Main.objects.get(Name="Game")
    if MainGame.Year == 2:
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "These berries also taste delicious. I will call them strawberries and tell the others they can eat them. This will certainly increase food per grass tile."
            MainGame.FoodForGrass = 6
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Did I just dodge a bullet? Or miss out on a great chance?"
    elif MainGame.Year == 4:
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "I have learned how to build a ship. Let's explore those wet tiles!"
            MainGame.Boat = True
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Most people in your village praise you for resisting this black magic. But a few also point out that a ship could have been usefull in discovering more of the world."

    MainGame.save()
