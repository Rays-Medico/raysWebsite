from django.urls import path
from . import views

app_name = 'health_vault'
urlpatterns = [
    path('', views.DocumentList.as_view(), name='index'),
    path('upload/', views.DocumentCreate.as_view(), name='upload_document'),
    path('<int:pk>/', views.DocumentDetail.as_view(), name='view_document'),
]