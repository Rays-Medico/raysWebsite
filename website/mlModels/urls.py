# urls.py updates
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mlModels, name='models'),
    path('parkinson/<int:result>/', views.parkinson, name='parkinson'),
    path('heartdisease/', views.heartdisease_home, name='heartdisease_home'),  # New URL pattern without result
    path('heartdisease/<int:result>/', views.heartdisease, name='heartdisease'),
    path('parkinson_predict/', views.parkinson_predict, name='parkinson_predict'),
    path('heartdisease_predict/', views.heartdisease_predict, name='heartdisease_predict'),
]