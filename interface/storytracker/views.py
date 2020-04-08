from django.shortcuts import render
from django.db import models

# Create your views here.

class TimeLine():

    def filtros(request):

        return render(request, 'filtros.html')

    def timeline(request):

        return render(request, 'timeline.html')