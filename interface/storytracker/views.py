from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PageRanking

# Create your views here.


class TimeLine():
    @csrf_exempt
    def filtros(request):

        return render(request, 'filtros.html')

    def timeline(request):

        return render(request, 'timeline.html')


class Ranking():
    
    @csrf_exempt
    def ranking(request):

        texto = request.POST.get("texto", "")
        data = request.POST.get("data", "")
        return JsonResponse(PageRanking().ranking(texto, data), safe=False)        
        
