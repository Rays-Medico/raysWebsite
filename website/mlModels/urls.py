from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.mlModels,name='models'),
    path('parkinson/',views.parkinson,name='parkinson'),
    path('heartdisease/',views.heartdisease, name='heartdisease'),
    path('parkinson_predict/', views.parkinson_predict,name='parkinson_predict'),
]
