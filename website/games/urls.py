from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.games,name='games'),
    path('mem_pat/',views.mem_pat,name='mem_pat'),
    path('reaction/',views.reaction,name='reaction'),
    path('lung_game/',views.lung_game,name='lung_game'),

]
