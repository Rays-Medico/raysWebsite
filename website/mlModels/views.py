from django.shortcuts import render
import numpy as np
import pickle
import os

# Get the base directory of your Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the path to store the model inside the 'models' folder
MODEL_PATH = os.path.join(BASE_DIR, "mlModels\models\parkinson.pkl")

# Save model
with open(MODEL_PATH,'rb') as f:
    model=pickle.load(f)

# Create your views here.
def mlModels(request):
    return render(request, 'models.html')

def parkinson(request):
    return render(request, 'parkinson.html')

def heartdisease(request):
    return render(request, 'heartdisease.html')

def parkinson_predict(request):
    features=[]
    if request.method == "POST":
        features = [
            float(request.POST["MDVP_Fo_Hz"]),
            float(request.POST["MDVP_Fhi_Hz"]),
            float(request.POST["MDVP_Flo_Hz"]),
            float(request.POST["MDVP_Jitter_percentage"]),
            float(request.POST["MDVP_Jitter_Abs"]),
            float(request.POST["MDVP_RAP"]),
            float(request.POST["Jitter_DDP"]),
            float(request.POST["MDVP_Shimmer"]),
            float(request.POST["MDVP_Shimmer_dB"]),
        ]
        
        data=np.array(features).reshape(1,-1)
        prediction=model.predict(data)[0]
        print(prediction)
    
    