# views.py updates
import base64
import io
import os
import cv2
import numpy as np
import tensorflow as tf
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.conf import settings
import pickle
from django.shortcuts import redirect
# Get the base directory of your Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the path to store the model inside the 'models' folder
MODEL_PATH = os.path.join(BASE_DIR, "mlModels", "models", "parkinson.pkl")

# Load the Parkinson's model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Create your views here.

def mlModels(request):
    return render(request, 'models.html')

def parkinson_home(request):
    return render(request, 'parkinson.html')

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
        
        data = np.array(features).reshape(1, -1)
        prediction = model.predict(data)[0]
        return redirect("parkinson_result", result=prediction)  
    # Use t
# Load the heart disease model
HEART_MODEL_PATH = os.path.join(BASE_DIR, "mlModels", "models", "heartdisease.pkl")

with open(HEART_MODEL_PATH, 'rb') as f:
    heart_disease_model = pickle.load(f)

def heartdisease_home(request):
    return render(request, 'heart_disease.html', {'result': None})

def heartdisease(request, result=None):
    return render(request, 'heart_disease.html', {'result': result})


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
        return redirect('heartdisease_result', result=prediction) 
    

class SkinCancerDetector:
    def __init__(self, model_path):
        """Initialize the detector with the trained model"""
        self.model = tf.keras.models.load_model(model_path)
        self.image_size = (224, 224)  # Model's expected input size

    def preprocess_image(self, image):
        """Preprocess the image for prediction"""
        img_array = np.array(image)
        img_resized = cv2.resize(img_array, self.image_size)
        img_normalized = img_resized / 255.0
        return np.expand_dims(img_normalized, axis=0)

    def predict(self, image):
        """Make prediction on the processed image"""
        processed_image = self.preprocess_image(image)
        prediction = self.model.predict(processed_image)
        return float(prediction[0][0])

def skincancer_home(request):
    return render(request, 'skincancer.html')
def skin_cancer_detection(request):
    context = {}
    
    # Initialize detector (lazy loading would be better for production)
    model_path = os.path.join(settings.BASE_DIR, 'mlModels', 'models', 'SkinCancer.h5')
    detector = SkinCancerDetector(model_path)
    
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        try:
            # Read and convert image
            image = Image.open(uploaded_file).convert('RGB')
            
            # Convert image to base64 for display
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            context['image_data'] = base64.b64encode(buffered.getvalue()).decode()
            context['original_size'] = f"{image.size[0]}x{image.size[1]}"
            
            # Make prediction
            risk_score = detector.predict(image)
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = "High Risk"
                color = "danger"
                recommendation = "Please consult a dermatologist immediately"
            elif risk_score > 0.4:
                risk_level = "Medium Risk"
                color = "warning"
                recommendation = "Recommend clinical evaluation"
            else:
                risk_level = "Low Risk"
                color = "success"
                recommendation = "No immediate concern, but regular checks advised"
            
            context.update({
                'show_result': True,
                'risk_score': f"{risk_score:.1%}",
                'risk_level': risk_level,
                'color_class': color,
                'recommendation': recommendation,
                'processed_size': f"{detector.image_size[0]}x{detector.image_size[1]}"
            })
            
        except Exception as e:
            context['error'] = f"Error processing image: {str(e)}"
    
    return render(request, 'skincancer.html', context)