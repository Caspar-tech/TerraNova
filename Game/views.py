from django.shortcuts import render, redirect
from .forms import UserRegisterForm 
from .models import Square
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
        Row = 3
        Column = 3

        context['Row'] = range(Row)
        context['Column'] = range(Column)
        context['Try'] = [0,1,2,3,4,5,6,7,8]

        return context

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
