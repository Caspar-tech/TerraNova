from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
from .models import Square
from django.views.generic import ListView

# Main-page render function
class MainView(ListView):
    model = Square
    template_name = "Game/main.html"
    context_object_name = "Square"

    # context = {
    #     "row": range(3),
    #     "column": range(3),
    # }
    # return render(request, 'Game/main.html', context)

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
