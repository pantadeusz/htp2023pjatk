from django.http import HttpResponse


def index(request):
    return HttpResponse("The API")

def predict(request):
    return HttpResponse("This will provide access to the prediction model")