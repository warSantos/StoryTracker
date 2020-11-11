from django.contrib import admin
from django.urls import path
from storytracker.views import (
    TimeLine,
    Ranking,
    Doc
)


urlpatterns = [
    path('', TimeLine.filtros, name='filtros'),
    path('pageranking/', Ranking.ranking, name='pageranking'),
    path('timeline/', TimeLine.timeline, name='timeline'),
    path('doc/', Doc.documentacao, name='doc')
]
