from django.db import models
from django.contrib.auth.models import User

class Square(models.Model):
    Row = models.IntegerField(default=0)
    Column = models.IntegerField(default=0)
    Terrain = models.TextField(default="Grass")

    def __str__(self):
        return str(self.Row) + "x" + str(self.Column)

class Main(models.Model):
    Name = models.TextField(default="Game")
    Rows = models.IntegerField(default=3)
    Columns = models.IntegerField(default=3)
    Testnumber = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Name)