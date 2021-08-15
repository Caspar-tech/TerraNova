from .models import (
    Main,
    Square
)

def Addup(FormInput):
    MainGame = Main.objects.get(Name="Game")
    Testnumber = MainGame.Testnumber
    Testnumber += int(FormInput.get("Rows"))
    MainGame.Testnumber = Testnumber
    MainGame.save()