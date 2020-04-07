from django.contrib import admin
from django.urls import path
from storytracker.views import (
    TimeLine
)


urlpatterns = [
    path('', TimeLine.home, name='home'),
]
