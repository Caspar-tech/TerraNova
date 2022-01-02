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
    Square.objects.filter(Save=False).delete()

    Rows = 10
    Columns = 10

    TerrainTypes = ["Grass", "Grass", "Water"]

    for r in range(Rows):
        for c in range(Columns):
            RandomTerrain = random.choice(TerrainTypes)
            Newtile = Square(Number=(r*Columns+c), Row=r, Column=c, Terrain=RandomTerrain, Save=False)
            Newtile.save()

    Center_square = Square.objects.get(Row=(Rows/2), Column=(Columns/2), Save=False)
    Center_square.Discovered = True
    Center_square.Terrain = "Grass"
    Center_square.save()

    MainGame = Main.objects.get(Name="Game")
    MainGame.Rows = Rows
    MainGame.Columns = Columns
    MainGame.Food = 100
    MainGame.Population = 100
    MainGame.Year = 0
    MainGame.NextYearBlock = False
    MainGame.Phase = 1
    MainGame.FoodForGrass = 4
    MainGame.FoodForWater = 9
    MainGame.FoodForFarm = 50
    MainGame.FarmEffectiveness = 0
    MainGame.StartEvent = False
    MainGame.EndEvent = False
    MainGame.Farmers = 0
    MainGame.Soldiers = 0
    MainGame.Idle = 0
    MainGame.OccupationsAreSet = False
    MainGame.Boat = False
    MainGame.Berry = False
    MainGame.Sacrifice = False
    MainGame.GameEnded = False
    MainGame.SubmitHighScore = False
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

def ClickSquare(FormInput):
    # When a tile is clicked on the grid in the html template
    # this functions checks whether a neighbour is already discovered
    # If this is true it "discovers" the clicked tile and reveals the terrain

    # But first we check if the tile is water and boating is already discovered and,
    # then we check if the clicked tile really is undiscovered
    Tileoption = FormInput.get("Tileoption")
    Clicked_square = int(FormInput.get("Square"))

    if Tileoption == "Discover":
        MainGame = Main.objects.get(Name="Game")
        if Square.objects.get(Number=Clicked_square, Save=False).Discovered == False:
            Neighbour_list = Who_are_my_neighbours(Clicked_square)

            Neighbour_discovered = False
            for i in Neighbour_list:
                if Square.objects.get(Number=i, Save=False).Discovered == True:
                    Neighbour_discovered = True

            if Neighbour_discovered == True:
                # Check if player has enough food to discover
                if MainGame.Price_discover_tile <= MainGame.Food:

                    Tile = Square.objects.get(Number=Clicked_square, Save=False)
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
    elif Tileoption == "Build Farm":
        MainGame = Main.objects.get(Name="Game")
        Tile = Square.objects.get(Number=Clicked_square, Save=False)

        if Tile.Discovered == False:
            Infobox("You can only build a farm on an explored tile")
            return

        if Tile.Terrain != "Grass":
            Infobox("You can only build a farm on an empty grass tile")
            return

        if MainGame.PriceBuildFarm > MainGame.Food:
            Infobox("Insufficient food ({0}) to build a farm".format(Main.objects.get(Name="Game").PriceBuildFarm))
            return

        Tile.Terrain = "Farm"
        Tile.save()
        MainGame.Food -= MainGame.PriceBuildFarm
        MainGame.save()
        Infobox("You built a farm")
    elif Tileoption == "Demolish Farm":
        MainGame = Main.objects.get(Name="Game")
        Tile = Square.objects.get(Number=Clicked_square, Save=False)

        if Tile.Discovered == False:
            Infobox("You can only demolish a farm on an explored tile")
            return

        if Tile.Terrain != "Farm":
            Infobox("You can only demolish a farm on a tile your previously build a farm on")
            return

        Tile.Terrain = "Grass"
        Tile.save()
        MainGame.save()
        Infobox("You demolished a farm")

def Who_are_my_neighbours(Number):
    # When a tile is clicked on the grid in the html template
    # This function returns a list of the number of the neighbour tiles
    Columns = Main.objects.get(Name="Game").Columns
    Rows = Main.objects.get(Name="Game").Rows
    Column = Square.objects.get(Number=Number, Save=False).Column
    Row = Square.objects.get(Number=Number, Save=False).Row

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

    if MainGame.StartEvent == True:
        MainGame.NextYearBlock = True
        MainGame.save()
        Infobox("Before starting a new year you must make a choice on the dilemma in the overview")
        return

    if MainGame.OccupationsAreSet == False and MainGame.Phase > 1:
        MainGame.NextYearBlock = True
        MainGame.save()
        Infobox("Before starting a new year you must set the occupations of your population")
        return

    MainGame.NextYearBlock = False
    MainGame.OccupationsAreSet = False

    MainGame.Year += 1

    MainGame.EndEvent = False

    FormerFood = MainGame.Food
    # Adding Water and Grass food
    NumberOfGrassTiles = len(Square.objects.filter(Discovered=True, Save=False).filter(Terrain="Grass"))
    NumberOfWaterTiles = len(Square.objects.filter(Discovered=True, Save=False).filter(Terrain="Water"))

    MainGame.NumberOfGrassTiles = NumberOfGrassTiles
    MainGame.NumberOfWaterTiles = NumberOfWaterTiles

    MainGame.Food += (NumberOfGrassTiles * MainGame.FoodForGrass)
    MainGame.Food += (NumberOfWaterTiles * MainGame.FoodForWater)

    MainGame.FoodForGrassCurrentYear = MainGame.FoodForGrass
    MainGame.FoodForWaterCurrentYear = MainGame.FoodForWater

    # Adding Farm food
    # Depends on how many farmers. 25 are needed per farm. Exponential effectivity.
    Farmers = MainGame.Farmers
    NumberOfFarmTiles = len(Square.objects.filter(Discovered=True, Save=False).filter(Terrain="Farm"))

    if NumberOfFarmTiles > 0:
        FarmersNeeded = NumberOfFarmTiles * 25

        FarmerPercentage = Farmers / FarmersNeeded

        FarmEffectiveness = FarmerPercentage * FarmerPercentage
        if FarmEffectiveness > 1:
            FarmEffectiveness = 1

        MainGame.FarmEffectiveness = FarmEffectiveness * 100

        MainGame.NumberOfFarmTiles = NumberOfFarmTiles
        MainGame.FarmFoodGained = round(NumberOfFarmTiles * MainGame.FoodForFarm * FarmEffectiveness)
        MainGame.Food += MainGame.FarmFoodGained
        MainGame.FoodForFarmCurrentYear = MainGame.FoodForFarm

    # Subtracting food and in- or decreasing population
    MainGame.PopulationLastYear = MainGame.Population

    if MainGame.Phase > 1:
        MainGame.Food -= MainGame.Population
        if MainGame.Food > 0:
            MainGame.Population += round(MainGame.Idle * 0.5)
        elif MainGame.Food < 0:
            MainGame.Population += MainGame.Food
            MainGame.Food = 0

    MainGame.PopulationChange = MainGame.Population - MainGame.PopulationLastYear
    MainGame.FoodGained = MainGame.Food - FormerFood
    MainGame.save()

    StartEvent()

def StartEvent():
    MainGame = Main.objects.get(Name="Game")

    if MainGame.Year == 2:
        MainGame.TextEvent = "These berries look delicious!"
        MainGame.EventButton1 = "Eat them"
        MainGame.EventButton2 = "Probably also poisonous"
        MainGame.StartEvent = True
    elif MainGame.Year == 4:
        MainGame.TextEvent = "A man on a wooden floating device comes your way from an undiscovered tile. " \
                             "He offers you his knowledge of this so called 'boat'"
        MainGame.EventButton1 = "Please, explain"
        MainGame.EventButton2 = "No, sounds like witchcraft!"
        MainGame.StartEvent = True
    elif MainGame.Year == 6:
        MainGame.TextEvent = "The high priest comes to you: 'The gods are not pleased with us. " \
                             "We only take from the land but we never give back. " \
                             "We should start sacrificing food on regular basis to the gods. " \
                             "This way we show how gratefull we are and we will please the gods.'"
        MainGame.EventButton1 = "Okay"
        MainGame.EventButton2 = "No, gods don't need food"
        MainGame.StartEvent = True
    elif MainGame.Year == 8:
        MainGame.TextEvent = "A group of fierce looking man approach your village by boat. " \
                             "They have helmets with horns and big axes. They seem dangerous..."
        MainGame.EventButton1 = "Hide in the hills"
        MainGame.EventButton2 = "Defend the village"
        MainGame.StartEvent = True
    elif MainGame.Year == 10:
        if MainGame.Food < 500:
            MainGame.GameEnded = True
            MainGame.SubmitHighscore = True
        else:
            MainGame.Phase += 1

    MainGame.save()

def EndEvent(FormInput):
    MainGame = Main.objects.get(Name="Game")
    if MainGame.Year == 2:
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "These berries also taste delicious. " \
                                    "I will call them strawberries and tell the others they can eat them. " \
                                    "This will certainly increase food per grass tile."
            MainGame.FoodForGrass = 6
            MainGame.Berry = True
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Did I just dodge a bullet? Or miss out on a great chance?"
    elif MainGame.Year == 4:
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "I have learned how to build a boat. Let's explore those wet tiles!"
            MainGame.Boat = True
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Most people in your village praise you for resisting this black magic. " \
                                    "But a few also point out that a boat could have " \
                                    "been usefull in discovering more of the world."
    elif MainGame.Year == 6:
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "The priest assures you the gods are pleased. " \
                                    "Sadly enough the people of your tribe seem more hungry"
            MainGame.FoodForGrass -= 1
            MainGame.FoodForWater -= 1
            MainGame.Sacrifice = True
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "The priest is mad and assures you the gods will be too. " \
                                    "But the people in your tribe don't seem to mind the extra food in their bellies."
    elif MainGame.Year == 8:
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "The 'vikings' steal 40 food but everybody is still alive."
            MainGame.Food -= 40
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Your tribesman are no match for the 'vikings'. " \
                                    "After a few of your friends are killed you surrender the village. " \
                                    "The vikings force you to tell them where the food is hidden." \
                                    "They take 100 food. " \
                                    "But Luckily the vikings are on a tight schedule, no time to burn your village. "
            MainGame.Food -= 100

    MainGame.save()

def SetNewHighscore(FormInput):
    MainGame = Main.objects.get(Name="Game")

    Name = FormInput.get("Name")
    Food = MainGame.Food

    Highscore.objects.create(Name=Name, Food=Food)

    MainGame.SubmitHighscore = False

    MainGame.save()

def Save():
    Square.objects.filter(Save=True).delete()

    Tiles = Square.objects.all()
    for i in Tiles:
        CopySaveTile = Square(Number=i.Number, Row=i.Row, Column=i.Column, Terrain=i.Terrain,
                              Discovered=i.Discovered, Save=True)
        CopySaveTile.save()

    try:
        Main.objects.get(Name="Save").delete()
    except:
        print("No savegame detected to delete")

    SaveGame = Main.objects.get(Name="Game")
    SaveGame.pk += 1
    SaveGame.Name = "Save"
    SaveGame.save()

    Infobox("Game was successfully saved")

def Load():
    if Main.objects.filter(Name="Save").exists():
        Square.objects.filter(Save=False).delete()

        Tiles = Square.objects.all()
        for i in Tiles:
            CopySaveTile = Square(Number=i.Number, Row=i.Row, Column=i.Column, Terrain=i.Terrain,
                                  Discovered=i.Discovered, Save=False)
            CopySaveTile.save()

        Main.objects.get(Name="Game").delete()

        MainGame = Main.objects.get(Name="Save")
        MainGame.pk += 1
        MainGame.Name = "Game"
        MainGame.save()

        Infobox("Game was successfully loaded")
    else:
        Infobox("There is no save game yet")

def SetOccupations(FormInput):
    # test whether the input are integers
    try:
        Farmers = int(FormInput.get('Farmers'))
        Soldiers = int(FormInput.get('Soldiers'))
    except:
        Infobox("Please only use numbers when selecting the number of farmers and soldiers")
        return

    MainGame = Main.objects.get(Name="Game")

    if MainGame.Population < (Farmers + Soldiers):
        Infobox("The number of farmers and soldiers you select should always be equal too or smaller than "
                "the seize of your population")
        return

    MainGame.Farmers = Farmers
    MainGame.Soldiers = Soldiers
    MainGame.Idle = MainGame.Population - Farmers - Soldiers

    MainGame.OccupationsAreSet = True

    MainGame.save()