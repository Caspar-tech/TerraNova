from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
#from .models import <name database>

# Main-page render funtcion
def main(request):
    context = {
        "A": "B",
        "row": range(5),
        "column": range(6),
    }
    return render(request, 'Game/main.html', context)

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
