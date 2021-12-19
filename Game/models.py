from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Square(models.Model):
    Number = models.IntegerField(default=0)
    Row = models.IntegerField(default=0)
    Column = models.IntegerField(default=0)
    Terrain = models.TextField(default="Grass")
    Discovered = models.BooleanField(default=False)
    Save = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Row) + "x" + str(self.Column)

class Main(models.Model):
    Name = models.TextField(default="Game")
    Rows = models.IntegerField(default=3)
    Columns = models.IntegerField(default=3)
    Food = models.IntegerField(default=100)
    Year = models.IntegerField(default=0)
    Phase = models.IntegerField(default=1)
    Price_discover_tile = models.IntegerField(default=20)
    PriceBuildFarm = models.IntegerField(default=50)
    Infobox = models.TextField(default="hello there-second line-third line")
    NumberOfGrassTiles = models.IntegerField(default=1)
    NumberOfWaterTiles = models.IntegerField(default=0)
    NumberOfFarmTiles = models.IntegerField(default=0)
    FoodForGrass = models.IntegerField(default=5)
    FoodForWater = models.IntegerField(default=0)
    FoodForFarm = models.IntegerField(default=25)
    FoodForGrassCurrentYear = models.IntegerField(default=5)
    FoodForWaterCurrentYear = models.IntegerField(default=0)
    FoodForFarmCurrentYear = models.IntegerField(default=25)
    StartEvent = models.BooleanField(default=False)
    EndEvent = models.BooleanField(default=False)
    TextEvent = models.TextField(default="Default text")
    TextEndEvent = models.TextField(default="Default EndText")
    EventButton1 = models.TextField(default="B1")
    EventButton2 = models.TextField(default="B2")
    Boat = models.BooleanField(default=False)
    Berry = models.BooleanField(default=False)
    Sacrifice = models.BooleanField(default=False)
    GameEnded = models.BooleanField(default=False)
    GameEndedSucces = models.BooleanField(default=False)
    GameEndedHighscore = models.BooleanField(default=False)
    Testnumber = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Name)

class Highscore(models.Model):
    Name = models.TextField(default="Anonymous")
    Food = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Name)