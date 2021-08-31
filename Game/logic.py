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
    print(Center_square.Number)
    Center_square.Discovered = True
    Center_square.save()

    MainGame = Main.objects.get(Name="Game")
    MainGame.Rows = Rows
    MainGame.Columns = Columns
    MainGame.Money = 100
    MainGame.Year = 0
    MainGame.save()

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
            # Check if player has enough money to discover
            if Money_check(Main.objects.get(Name="Game").Price_discover_tile):
                Tile = Square.objects.get(Number=Clicked_square)
                Tile.Discovered = True
                Tile.save()
        else:
            print("No adjacent tile discovered yet")

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

def Money_check(Price):
    MainData = Main.objects.get(Name="Game")

    if MainData.Money < Price:
        print("insufficient funds")
        return False
    else:
        MainData.Money -= Price
        MainData.save()
        return True

