from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
from .models import Square, Main
from django.views.generic import ListView

from .logic import (
    Newgrid,
    Discover,
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
        for i in Square.objects.all():
            if i.Discovered == True:
                Square_terrain.append(i.Terrain)
            else:
                Square_terrain.append("Undiscovered")
        context['Square_terrain'] = Square_terrain

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('Create') == 'Create':
            # Creates a new grid, using given Rows and Columns
            Newgrid(request.POST)
        elif request.POST.get('Next Year') == 'Next Year':
            return redirect('overview')
        elif request.POST.get('Square') != "":
            # Sets the clicked tile from undiscovered to discovered (if a neighbour is discovered)
            Discover(int(request.POST.get('Square')))
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

    def post(self, request, *args, **kwargs):
        if request.POST.get('Return') == 'Return':
            return redirect('main')
        return super().get(request, *args, **kwargs)