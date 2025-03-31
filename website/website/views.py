from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about_us.html')

def contact(request):
    return render(request,'contact_us.html')

def streamlit_view(request):
    return render(request, 'streamlit_embed.html')

def chatbot(request):
    return render(request, 'chatbot.html')

# def model(request):
#     return render(request, 'models.html')

def parkinson(request):
    return render(request, 'parkinson.html')

def cancer(request):
    return render(request, 'cancer.html')

def heartdisease(request):
    return render(request, 'heartdisease.html')

def chatbot_nav(request):
    return render(request, 'chatbot_nav.html')