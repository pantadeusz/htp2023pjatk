from django.http import HttpResponse
from django.http import JsonResponse
import sys

sys.path.append('../')
from ai import ai_model

def index(request):
    return HttpResponse("The API")

def predict(request):
    steps_back = 0
    print(request.GET)
    if (request.GET):
        steps_back = int(request.GET.get('steps_back', 0))
    print (steps_back)
    try:
        return JsonResponse(ai_model.do_the_prediction(steps_back,input_datapoints='../ai/data/datapoints2023.csv', model_path='../ai/keras_predict_model', exclude_places=set(['5b', '5c'])))
    except:
        return HttpResponse('{"error":"FAIL... See logs"}')