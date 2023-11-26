from django.shortcuts import render, redirect,  get_object_or_404
from .forms import FarmActivityAddForm
from .models import Farm, Measurement, SensorType

from .serial_connection import start_measurement_thread
from django.http import JsonResponse


start_measurement_thread()


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


def read_sensor(request):
    measurements = Measurement.objects.all()
    sensor_types = [sensor_type[0] for sensor_type in SensorType.choices]

    data = {}
    for sensor_type in sensor_types:
        sensor_measurements = measurements.filter(sensor_type=sensor_type)
        data[sensor_type] = [
            {'x': measurement.date_time.timestamp(), 'y': measurement.detected_number} for
            measurement in sensor_measurements]

    context = {'data': data}
    return render(request, 'farm_management/chart.html', context)


def alert_status(request):
    measurements = Measurement.objects.last()
    print("Last measurement from database", measurements)

    alert_status = False
    if measurements.detected_number > 600:
        alert_status = True

    context = {'sensor_value': measurements.detected_number,
               'alert': alert_status
               }
    return JsonResponse(context)


