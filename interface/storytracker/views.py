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
    
    @csrf_exempt
    def timeline(request):
        id_doc = request.POST.get("id_doc", "")
        print("ID Documento Selecionado: ", id_doc)
        
        return render(request, 'timeline.html')


class Ranking():
    
    @csrf_exempt
    def ranking(request):

        texto = request.POST.get("texto", "")
        data = request.POST.get("data", "")
        meses = request.POST.get("meses", "")
        return JsonResponse(PageRanking().ranking(texto, data), safe=False)     
        

class Doc():

    def documentacao(request):
        return render(request, "doc.html")