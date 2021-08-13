from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
from .models import Square, Main
from django.views.generic import ListView

# Main-page render function
class MainView(ListView):
    model = Square
    template_name = "Game/main.html"
    context_object_name = "Square"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in QuerySets of extra context
        Rows = Main.objects.get(Name="Game").Rows
        Columns = Main.objects.get(Name="Game").Columns

        context['Rows'] = range(Rows)
        context['Columns'] = range(Columns)

        Square_terrain = []
        for i in Square.objects.all():
            Square_terrain.append(i.Terrain)
        context['Square_terrain'] = Square_terrain

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('Create') == 'Create':
            return redirect('login')
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
