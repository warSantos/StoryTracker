from django.shortcuts import render
from django.db import models

# Create your views here.

class TimeLine():

    def home(request):

        return render(request, 'timeline.html')