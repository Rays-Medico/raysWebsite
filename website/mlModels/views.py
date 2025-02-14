from django.shortcuts import render,redirect
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

def parkinson(request, result):
    return render(request, 'parkinson.html', {'result': result})

def parkinson_predict(request):
    features = []
    if request.method == "POST":
        features = [
        float(request.POST["MDVP_Fo_Hz"]),
        float(request.POST["MDVP_Fhi_Hz"]),
        float(request.POST["MDVP_Flo_Hz"]),
        float(request.POST["MDVP_Jitter_percentage"]),
        float(request.POST["MDVP_Jitter_Abs"]),
        float(request.POST["MDVP_RAP"]),
        float(request.POST["MDVP_PPQ"]),
        float(request.POST["Jitter_DDP"]),
        float(request.POST["MDVP_Shimmer"]),
        float(request.POST["MDVP_Shimmer_dB"]),
        float(request.POST["Shimmer_APQ3"]),
        float(request.POST["Shimmer_APQ5"]),
        float(request.POST["MDVP_APQ"]),
        float(request.POST["Shimmer_DDA"]),
        float(request.POST["NHR"]),
        float(request.POST["HNR"]),
        float(request.POST["RPDE"]),
        float(request.POST["DFA"]),
        float(request.POST["spread1"]),
        float(request.POST["spread2"]),
        float(request.POST["D2"]),
        float(request.POST["PPE"]),
    ]

        
        data=np.array(features).reshape(1,-1)
        prediction=model.predict(data)[0]
        return redirect("parkinson", result=prediction)

    
from django.shortcuts import render
import numpy as np
import pickle
import os

# Load the heart disease model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "mlModels", "models", "heartdisease.pkl")

with open(MODEL_PATH, 'rb') as f:
    heart_disease_model = pickle.load(f)

def heartdisease(request, result):
    return render(request, 'heart_disease.html', {'result':result})

def heartdisease_predict(request):
    if request.method == "POST":
            # Extract form data
            features = [
                int(request.POST["age"]),
                1 if request.POST["gender"] == "Male" else 0,
                int(request.POST["cp"]),
                int(request.POST["trestbps"]),
                int(request.POST["chol"]),
                1 if request.POST["fbs"] == "True" else 0,
                int(request.POST["restecg"]),
                int(request.POST["thalach"]),
                1 if request.POST["exang"] == "Yes" else 0,
                float(request.POST["oldpeak"]),
                int(request.POST["slope"]),
                int(request.POST["ca"]),
                {"Normal": 1, "Fixed defect": 2, "Reversable defect": 3}.get(request.POST["thal"], 1),
            ]

            # Make prediction
            prediction = heart_disease_model.predict(np.array([features]))[0]
            result = prediction
            return redirect('heartdisease',result=result)
           

    return render(request, "heartdisease.html")
