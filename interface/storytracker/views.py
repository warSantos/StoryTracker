import json
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
        
        # Convertendo o json para dicionário.
        info = json.loads(request.POST.get("info", ""))
        print(info)
        # Fazendo requisição da timline.
        tm = TimelineModel()
        data = {}
        data["documentos"] = tm.timeline(info)
        #return JsonResponse(docs_tm, safe=False)     
        return render(request, 'timeline.html', data)


class Ranking():
    
    @csrf_exempt
    def ranking(request):

        texto = request.POST.get("texto", "")
        data = request.POST.get("data", "")
        meses = int(request.POST.get("meses", ""))
        n_docs = int(request.POST.get("n_docs",""))
        classes = request.POST.get("classes","")#.split(',')
        print(texto,data,meses,n_docs,classes)

        return JsonResponse(PageRanking().ranking(texto, data, meses, n_docs, classes), safe=False)     
        

class Doc():

    def documentacao(request):
        
        return render(request, "doc.html")