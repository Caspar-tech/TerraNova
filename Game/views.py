from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
from .models import Square, Main, Highscore
from django.views.generic import ListView

from .logic import (
    Newgrid,
    ClickSquare,
    NextYear,
    StartEvent,
    EndEvent,
    SetNewHighscore,
    Save,
    Load,
    SetOccupations,
)

# Main-page render function
class MainView(ListView):
    model = Square
    template_name = "Game/main.html"
    context_object_name = "Square"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['Main'] = Main.objects.get(Name="Game")

        context['Infobox'] = (Main.objects.get(Name="Game").Infobox).split("-")

        # Add in QuerySets of extra context
        Rows = Main.objects.get(Name="Game").Rows
        Columns = Main.objects.get(Name="Game").Columns

        context['RowsRange'] = range(Rows)
        context['ColumnsRange'] = range(Columns)
        context['Columns'] = Columns

        # We run trough all the squares in the database
        # We create a list of all terrain types, so we can iterate over them in the html template
        # Only discovered tiles reveal their terrain, else "undiscovered" is added to the list
        Square_terrain = []
        Numbers = []
        for i in Square.objects.filter(Save=False).order_by("Number"):
            if i.Discovered == True:
                Square_terrain.append(i.Terrain)
            else:
                Square_terrain.append("Undiscovered")
            Numbers.append(i.Number)
        context['Square_terrain'] = Square_terrain
        context['Numbers'] = Numbers

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('Start new game') == 'Start new game':
            # Creates a new grid, using given Rows and Columns
            Newgrid()
        elif request.POST.get('Save') == 'Save':
            Save()
        elif request.POST.get('Load') == 'Load':
            Load()
        elif request.POST.get('Set occupations') == 'Set occupations':
            SetOccupations(request.POST)
        elif request.POST.get('Next Year') == 'Next Year':
            NextYear()
            if Main.objects.get(Name="Game").NextYearBlock == False:
                return redirect('overview')
        elif request.POST.get('End Game') == 'End Game':
            return redirect('end')
        elif request.POST.get('Square') != "":
            # Sets the clicked tile from undiscovered to discovered (if a neighbour is discovered)
            ClickSquare(request.POST)
        return super().get(request, *args, **kwargs)

#Register-page render function
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = UserRegisterForm()
    return render(request, 'Game/register.html', {'form': form})

class OverviewView(ListView):
    model = Square
    template_name = "Game/overview.html"
    context_object_name = "Square"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['Main'] = Main.objects.get(Name="Game")
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('Return') == 'Return':
            return redirect('main')
        elif request.POST.get('End Game') == 'End Game':
            return redirect('end')
        elif request.POST.get('EventButton') != "":
            EndEvent(request.POST)
        return super().get(request, *args, **kwargs)

class EndView(ListView):
    model = Square
    template_name = "Game/end.html"
    context_object_name = "Square"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['Main'] = Main.objects.get(Name="Game")
        context['Highscore'] = Highscore.objects.all().order_by("-Food")
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('Start new game') == 'Start new game':
            Newgrid()
            return redirect('main')
        elif request.POST.get('Submit Highscore') == 'Submit Highscore':
            SetNewHighscore(request.POST)
        return super().get(request, *args, **kwargs)