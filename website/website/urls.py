"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('streamlit/', views.streamlit_view, name='streamlit_embed'),
    #TODO: Add a new path for the streamlit chatbot
    path('chatbot/', views.chatbot, name='chatbot'),
    # path('models/', views.model, name='models'),
    path('parkinson/', views.parkinson, name='parkinson'),
    path('cancer/', views.cancer, name='cancer'),
    path('heartdisease/', views.heartdisease, name='heartdisease'),
    path('games/', include('games.urls'),name='games'),
    path('models/', include('mlModels.urls'), name='models'),
]
