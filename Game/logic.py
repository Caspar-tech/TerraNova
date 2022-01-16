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
    MainGame.EventList = "1-2-3-4-5-6-7-8-9-10"
    MainGame.Farmers = 0
    MainGame.Soldiers = 0
    MainGame.SoldiersEffectiveness = 100
    MainGame.Idle = 0
    MainGame.OccupationsAreSet = False
    MainGame.Boat = False
    MainGame.Berry = False
    MainGame.Sacrifice = False
    MainGame.Writing = ""
    MainGame.Pyramid = False
    MainGame.Trojan = False
    MainGame.Codex = False
    MainGame.Smith = ""
    MainGame.Leadership = ""
    MainGame.Christianity = False
    MainGame.Wall = False
    MainGame.GameEnded = False
    MainGame.SubmitHighScore = False
    MainGame.War = False
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

    # After the year is rounded up, there is the possibility of a war (phase > 0)
    War()

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

    if MainGame.Year > 10:

        # 1 in 5 times we pick one of the events that has not happened yet.
        # Make from a textfield in the model a list and than reverse again
        if MainGame.EventList == "":
            return

        if random.randint(1, 5) != 1:
            ### DELETE after testing
            # return
            pass

        EventList = (MainGame.EventList).split("-")

        MainGame.CurrentEvent = random.choice(EventList)

        EventListString = ""
        for i in EventList:
            if i != MainGame.CurrentEvent:
                EventListString += i + "-"
        EventListString = EventListString[:-1]

        MainGame.EventList = EventListString

        ### DELETE after testing
        MainGame.CurrentEvent = "10"

        # Now follow the actual events
        if MainGame.CurrentEvent == "1":
            MainGame.TextEvent = "An old man in a white robe visits your village. He says he has spend his life " \
                                 "studying the art of putting words into writing. This sounds very useful to you. " \
                                 "Often you forget where you placed your sword. If you could just write it down it " \
                                 "would save you many hours of searching. The old man offers you to teach you one " \
                                 "script. Which do you want to learn?"
            MainGame.EventButton1 = "Sumerian Cuneiform"
            MainGame.EventButton2 = "Akkadian Cuneiform"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "2":
            MainGame.TextEvent = "During one of your travels you meet a man named Imhotep. He says he is an architect." \
                                 " Which turns out to be a fancy word for someone who thinks of houses but does not " \
                                 "actually build them himself. He offers to build you a triangular burial tomb."
            MainGame.EventButton1 = "Yes"
            MainGame.EventButton2 = "No"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "3":
            MainGame.TextEvent = "This week two messengers arrived in your village. One is send by a king named" \
                                 " Priamus and the other by a great leader called Agamemnon. Something about someone’s " \
                                 "wife being stolen and now everybody is upset. Both messengers humbly ask you to " \
                                 "support their cause in the upcoming war. Your soldiers could use some training so " \
                                 "why not. Which king will you support?"
            MainGame.EventButton1 = "Priamus"
            MainGame.EventButton2 = "Agamemnon"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "4":
            MainGame.TextEvent = "One day a special envoy of king Hammurabi presents himself to you. He tells " \
                                 "about a very useful tool that has been developed: the codex. This is a book " \
                                 "that contains all the rules of the land. The envoy tells you that all great " \
                                 "leaders have a codex these days. Are you interested in receiving a copy " \
                                 "and declaring it law?"
            MainGame.EventButton1 = "Yes"
            MainGame.EventButton2 = "No"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "5":
            MainGame.TextEvent = "A strong muscled man arrives in your village. His traveling party was raided by " \
                                 "bandits and he only narrowly escaped death. The friendly leader you are, you " \
                                 "offer the man food and shelter. After a while he finds back his strength and " \
                                 "offers you a gift in return. He will let you in on the knowledge of bronze or" \
                                 " copper making to replace your leather and stone outfits. " \
                                 "Which process you find most interesting?"
            MainGame.EventButton1 = "Bronze"
            MainGame.EventButton2 = "Copper"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "6":
            MainGame.TextEvent = "You have become aware of a phenomenon called the Olympic games. Once every " \
                                 "four years your distant neighbours of the Greek city states come together to " \
                                 "participate in all kinds of tiring activities. These “games” itself don’t " \
                                 "interest you but they do seem to present a possibility. The closest " \
                                 "participant - the city of Megara - is left pretty much undefended during " \
                                 "the games. You could disguise your soldiers and raid the city next time or you " \
                                 "could ask to participate in the games and maybe make some friends."
            MainGame.EventButton1 = "Raid Megara"
            MainGame.EventButton2 = "Ask to participate"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "7":
            MainGame.TextEvent = "Travellers visiting your village tell you about a large empire, called the Roman " \
                                 "empire, which is at struggle with itself. The empire has long been ruled by a " \
                                 "group of elected man called the senate. But this so called republic is now " \
                                 "being threatened by a general who claims himself to be the sole leader of the " \
                                 "empire. Both forms of government seem interesting, what role do you prefer?"
            MainGame.EventButton1 = "President of the senate"
            MainGame.EventButton2 = "Caesar (Emperor)"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "8":
            MainGame.TextEvent = "For as long as you can remember your village has been relying on the local " \
                                 "shaman for spiritual guidance. On his advice every second full moon you sacrifice " \
                                 "a hand full of berries to the fire and water gods to prevent natural disaster and " \
                                 "deceases. Which works okay but still didn’t prevent the floods last year. " \
                                 "Not along ago a priest came by to announce that Christianity is now the main " \
                                 "thing in most of the known world. Shall we adopt Christianity or stick with " \
                                 "the shaman?"
            MainGame.EventButton1 = "Shaman"
            MainGame.EventButton2 = "Christianity"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "9":
            MainGame.TextEvent = "One day in the middle of the day one of the farmers comes running into the village. " \
                                 "A huge army is slowly passing by his farm. He overheard the soldiers speaking " \
                                 "of an Alexander the Great invading foreign places like Egypt and India. " \
                                 "Shall we hide in the village and pretend we are not there or invite this " \
                                 "Alexander over for dinner?"
            MainGame.EventButton1 = "Hide in the village"
            MainGame.EventButton2 = "Invite Alexander"
            MainGame.StartEvent = True
        elif MainGame.CurrentEvent == "10":
            MainGame.TextEvent = "A merchant by the name of Lu Buwei visits your village for a stay overnight " \
                                 "during his travel. He works for a mighty emperor named Qin Shi Huang. He claims " \
                                 "that this emperor has build a wall which – if it were to exist – could be seen by " \
                                 "an eye high up in in the sky. Although crazy expensive it works really well " \
                                 "for protecting his kingdom against enemies. The merchant is willing to help you " \
                                 "build a similar wall around your village, but it wont be cheap. " \
                                 "You estimate it will cost your around 90% of your food."
            MainGame.EventButton1 = "Build wall"
            MainGame.EventButton2 = "Don't build wall"
            MainGame.StartEvent = True

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
    elif MainGame.CurrentEvent == "1":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "The writing skills you have been taught proof to be very useful. You write down " \
                                    "instructions how to plough fields and what army formations have proven to be most " \
                                    "effective. But there is an itching feeling that writing could be done even more " \
                                    "effective. You are just not smart enough to improve it yourself. And where did " \
                                    "you place your sword…"
            MainGame.Writing = "Sumerian Cuneiform"
            MainGame.FoodForFarm += 5
            MainGame.SoldiersEffectiveness += 5
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "The writing skills you have been taught proof to be very useful. You write down " \
                                    "instructions how to plough fields and what army formations have proven to be most " \
                                    "effective. You are clearly using the state of the art writing system."
            MainGame.Writing = "Akkadian Cuneiform"
            MainGame.FoodForFarm += 10
            MainGame.SoldiersEffectiveness += 10
    elif MainGame.CurrentEvent == "2":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "Wow that looks great! Some villagers actually call it a wonder. And it is a very" \
                                    " comforting thought that your future corps will have a safe place to remain for" \
                                    " the rest of human existence. Just too bad that 20% of your population died" \
                                    " during the building of the pyramid as - volunteer -"
            MainGame.Pyramid = True
            MainGame.Population = round(MainGame.Population * 0.8)
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Seriously? You don’t want a pyramid? Architect Imhotep reacts unbelievingly. " \
                                    "But you don’t care. They can just put your future dead body in a Megaslithos. " \
                                    "That is good enough for you."
    elif MainGame.CurrentEvent == "3":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "It has been many years now and suddenly one of the soldiers you send returns home. " \
                                    "He claims to be the only survivor. But he seems to have gone mad as he explains " \
                                    "they were beaten by a wooden horse as big as a city. " \
                                    "Too bad about the soldiers lost though."
            MainGame.Population = round(MainGame.Population * 0.9)
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "It has been many years now and suddenly the soldiers you send return home. " \
                                    "They tell stories about a long and boring siege. Which ended when one of the " \
                                    "generals thought of a crafty trick of building a huge wooden horse. " \
                                    "You think it is a strange story and you suspect your soldiers of just " \
                                    "having been on holiday. On the other hand… they have learned some " \
                                    "very useful military strategies increasing their effectiveness. "
            MainGame.SoldiersEffectiveness += 5
            MainGame.Trojan = True
    elif MainGame.CurrentEvent == "4":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "The codex makes for great reading. It obligates all men to become soldier " \
                                    "and fight for their king when asked. Also the codex instates punishment for " \
                                    "all those farmers that neglect their farming duties. The fact that these rules " \
                                    "have now been written down makes them even more effective."
            MainGame.Codex = True
            MainGame.FoodForFarm += 5
            MainGame.SoldiersEffectiveness += 5
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "You beat off this early attempt at bureaucracy. Everybody in your village " \
                                    "knows the rules and if not there is always you to tell people what the " \
                                    "rules are. Sometimes this leads to minor misunderstandings but that " \
                                    "seems a better option than some boring codex."
    elif MainGame.CurrentEvent == "5":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "Amazing stuff, turns out that bronze is even better than copper. " \
                                    "Just adding a little tin to copper creates a sturdy alloy named bronze. " \
                                    "This will improve the effectiveness of your army greatly."
            MainGame.Smith = "Bronze"
            MainGame.SoldiersEffectiveness += 10
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "Nice stuff, clearly better and stronger than you were used to. " \
                                    "This will improve the effectiveness of your army."
            MainGame.Smith = "Copper"
            MainGame.SoldiersEffectiveness += 5
    elif MainGame.CurrentEvent == "6":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "The raid was a succes although there wasn't much to steal. " \
                                    "But apparently you have broken the ekecheiria which is a truce between all " \
                                    "participants in the Olympic games. The city states don’t take it lightly and " \
                                    "before you know it an impressive army arrives at your village. So much for your " \
                                    "soldiers disguising skills. You quickly pay a fine in the form of food " \
                                    "and - volunteers - to prevent annihilation."
            MainGame.Population = round(MainGame.Population * 0.8)
            MainGame.Food = round(MainGame.Food * 0.8)
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "The city states let your participate but it turns out your villagers are not " \
                                    "very athletic. With a 13th place in apene (mull cart racing) and 27th place " \
                                    "in pale (nude wrestling) being your best notations you become the laughing " \
                                    "stock of the participants."
    elif MainGame.CurrentEvent == "7":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "The people working the land feel represented by the elected senate. They are " \
                                    "motivated to work even harder. Better not tell them you fill out the election " \
                                    "results beforehand."
            MainGame.Leadership = "Republic"
            MainGame.FoodForFarm += 5
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "You soldiers feel motivated by the strong leader governing their village. " \
                                    "Your aura of power shines on them. Just make sure they don’t expect you to " \
                                    "actually lead them into battle."
            MainGame.Leadership = "Emperor"
            MainGame.SoldiersEffectiveness += 5
    elif MainGame.CurrentEvent == "8":
        MainGame.StartEvent = False
        MainGame.EndEvent = True
        if FormInput.get("EventButton") == "EventButton1":
            MainGame.TextEndEvent = "If you do what you did, you get what you got. Keep on sacrificing those berries."
        elif FormInput.get("EventButton") == "EventButton2":
            MainGame.TextEndEvent = "It took a while to get used to it but now all the villagers know what is " \
                                    "expected to keep the gods… uh god… happy. Ritual sacrifice is not needed " \
                                    "anymore. There is just one thing. Nobody is allowed to work anymore on " \
                                    "Sundays. That doesn’t help productivity."
            MainGame.Sacrifice = False
            MainGame.Christianity = True
            MainGame.FoodForFarm -= 5
    elif MainGame.CurrentEvent == "9":
            MainGame.StartEvent = False
            MainGame.EndEvent = True
            if FormInput.get("EventButton") == "EventButton1":
                MainGame.TextEndEvent = "After almost a day the army finally passed by. They didn’t notice or did " \
                                        "not care about your village. A little bit of food has disappeared but " \
                                        "nothing large. You wonder if you missed out on adventure or misfortune."
                MainGame.Food = round(MainGame.Food * 0.9)
            elif FormInput.get("EventButton") == "EventButton2":
                MainGame.TextEndEvent = "You walk towards the passing army and ask to speak to their leader. " \
                                        "Sadly enough you are just laughed at. Even worse one of the lower leaders " \
                                        "demands food for his soldiers. It is clear that if you don’t volunteer " \
                                        "the food you will loose it anyway. Maybe you should have hidden in the " \
                                        "village after all?"
                MainGame.Food = round(MainGame.Food * 0.5)
    elif MainGame.CurrentEvent == "10":
            MainGame.StartEvent = False
            MainGame.EndEvent = True
            if FormInput.get("EventButton") == "EventButton1":
                MainGame.TextEndEvent = "It really was a though job but with the expertise of the merchant the wall " \
                                        "now stands. This greatly increases the effectiveness of your army."
                MainGame.Food = round(MainGame.Food * 0.1)
                MainGame.SoldiersEffectiveness += 10
                MainGame.Wall = True
            elif FormInput.get("EventButton") == "EventButton2":
                MainGame.TextEndEvent = "The wall would have totally spoiled the view from your house anyway."

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

    Infobox("Game was saved successfully")

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

        Infobox("Game was loaded successfully ")
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

def War():
    MainGame = Main.objects.get(Name="Game")
    MainGame.War = False

    if MainGame.Phase == 1:
        MainGame.save()
        return

    WarChance = random.randint(1, 5)

    ### Delete after testing
    WarChance = 1

    if WarChance != 1:
        MainGame.save()
        return

    MainGame.War = True

    OpponentStrength = random.randint(20, 75)
    MainGame.WarOpponentSoldiers = round(MainGame.Population * (OpponentStrength / 100))

    MainGame.SoldiersEffectivenessCurrentYear = MainGame.SoldiersEffectiveness
    ArmyStrength = MainGame.Soldiers * (MainGame.SoldiersEffectiveness / 100)

    if ArmyStrength >= MainGame.WarOpponentSoldiers:
        MainGame.WarOutcome = "Win"
    else:
        MainGame.WarWon = False
        try:
            LooseRatio = (MainGame.WarOpponentSoldiers / ArmyStrength) - 1
        except:
            LooseRatio = 2
        if LooseRatio < 0.3:
            MainGame.WarOutcome = "Small loss"
            MainGame.WarFoodLost = round(MainGame.Food * 0.2)
            MainGame.WarPopulationLost = round(MainGame.Population * 0.02)
        elif LooseRatio < 0.6:
            MainGame.WarOutcome = "Significant loss"
            MainGame.WarFoodLost = round(MainGame.Food * 0.4)
            MainGame.WarPopulationLost = round(MainGame.Population * 0.1)
        else:
            MainGame.WarOutcome = "Huge loss"
            MainGame.WarFoodLost = round(MainGame.Food * 0.6)
            MainGame.WarPopulationLost = round(MainGame.Population * 0.3)

            if len(Square.objects.filter(Save=False, Discovered=True)) > 4:
                LostTiles = random.choices(Square.objects.filter(Save=False, Discovered=True), k=5)

                for n in LostTiles:
                    if n.Terrain == "Farm":
                        n.Terrain = "Grass"
                    n.Discovered = False
                    n.save()

        MainGame.Food -= MainGame.WarFoodLost
        MainGame.Population -= MainGame.WarPopulationLost

    MainGame.save()