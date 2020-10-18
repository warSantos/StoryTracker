from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PageRanking, TimelineModel

# Create your views here.


class TimeLine():
    
    @csrf_exempt
    def filtros(request):

        return render(request, 'filtros.html')
    
    @csrf_exempt
    def timeline(request):

        id_doc = int(request.POST.get("id_doc", "").replace("checkbox_",""))
        print("ID Documento Selecionado: ", id_doc)
        tm = TimelineModel()
        data = {}
        data["documentos"] = tm.timeline(id_doc)
        #return JsonResponse(docs_tm, safe=False)     
        return render(request, 'timeline.html', data)


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