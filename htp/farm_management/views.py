from django.shortcuts import render, redirect,  get_object_or_404
from .forms import FarmActivityAddForm
from .models import Farm


def farm_list(request):
    farms = Farm.objects.all()
    return render(request, 'farm_management/farm_list.html', {'farms': farms})


def farm_detail(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id)
    return render(request, 'farm_management/farm_detail.html', {'farm': farm})


def add_activity(request):
    if request.method == 'POST':
        form = FarmActivityAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farm_list')  # Redirect to the farm list page
    else:
        form = FarmActivityAddForm()

    return render(request, 'farm_management/add_activity.html', {'form': form})
