from django.shortcuts import render, redirect
from .forms import FarmActivityAddForm


def add_activity(request):
    if request.method == 'POST':
        form = FarmActivityAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farm_list')  # Redirect to the farm list page
    else:
        form = FarmActivityAddForm()

    return render(request, 'farm_management/add_activity.html', {'form': form})
