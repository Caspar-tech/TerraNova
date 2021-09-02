from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Square(models.Model):
    Number = models.IntegerField(default=0)
    Row = models.IntegerField(default=0)
    Column = models.IntegerField(default=0)
    Terrain = models.TextField(default="Grass")
    Discovered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Row) + "x" + str(self.Column)

class Main(models.Model):
    Name = models.TextField(default="Game")
    Rows = models.IntegerField(default=3)
    Columns = models.IntegerField(default=3)
    Money = models.IntegerField(default=100)
    Year = models.IntegerField(default=0)
    Price_discover_tile = models.IntegerField(default=20)
    Testnumber = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Name)