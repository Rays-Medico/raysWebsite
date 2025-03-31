# urls.py updates
from django.urls import path
from . import views


urlpatterns = [
    # Home and models page
    path('', views.mlModels, name='models_home'),
    
    path('', views.mlModels, name='models'),  # Change name to match your template
    
    # Heart Disease
    path('heartdisease/', views.heartdisease_home, name='heartdisease'),
    path('heartdisease/predict/', views.heartdisease_predict, name='heartdisease_predict'),
    path('heartdisease/<int:result>/', views.heartdisease, name='heartdisease_result'),
    
    # Parkinson's
    path('parkinson/', views.parkinson_home, name='parkinson'),
    path('parkinson/predict/', views.parkinson_predict, name='parkinson_predict'),
    path('parkinson/<int:result>/', views.parkinson, name='parkinson_result'),
    # Skin Cancer
    path('skincancer/', views.skincancer_home, name='skincancer'),
    path('skincancer/predict/', views.skin_cancer_detection, name='skincancer_predict'),
]