from django.shortcuts import render
from django.db import models
from .models import PageRanking

# Create your views here.

class TimeLine():

    def filtros(request):

        return render(request, 'filtros.html')

    def timeline(request):

        return render(request, 'timeline.html')

class Ranking():

    def ranking(request):

        texto = request.POST.get("texto","")
        data = request.POST.get("data","")
        vetores = PageRanking().ranking(texto, data)
        data = {}
        data["vetores"] = vetores
        return data