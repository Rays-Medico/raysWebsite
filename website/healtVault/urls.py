from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'healthVault'  # Ensure this matches your app directory name
urlpatterns = [
    path('',views.vault, name='vault'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('success/', lambda request: render(request, 'success.html'), name='pdf_success'),
    # path('test_upload/', views.test_upload, name='test_upload'),
    # path('check_model_storage/', views.check_model_storage, name='check_model_storage'),
]