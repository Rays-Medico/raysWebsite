from django.db import models
from django.conf import settings
# Create your models here.
class Parkinson(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,
                           on_delete=models.CASCADE,
                           related_name='parkinson'
                           )
    name=models.CharField(max_length=10)
    mdvp_fo_hz  =   models.FloatField()  
    mdvp_fhi_hz  =  models.FloatField() 
    mdvp_flo_hz  =  models.FloatField()
    mdvp_jitter_percentage  =   models.FloatField()
    mdvp_jitter_abs  =  models.FloatField()
    mdvp_rap  = models.FloatField()
    mdvp_ppq  = models.FloatField()
    jitter_ddp  =   models.FloatField()
    mdvp_shimmer  = models.FloatField()
    mdvp_shimmer_db  =  models.FloatField()
    shimmer_apq3  = models.FloatField()
    shimmer_apq5  = models.FloatField()
    mdvp_apq  = models.FloatField()
    shimmer_dda  =  models.FloatField()
    nhr  =  models.FloatField()
    hnr  =  models.FloatField()
    rpde  = models.FloatField()
    dfa  =  models.FloatField()
    spread1  =  models.FloatField()
    spread2  =  models.FloatField()
    d2  =   models.FloatField()
    ppe  =  models.FloatField()
    prediction_result = models.CharField(max_length=20)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.name} - {self.prediction_result}"


class HeartDisease(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='heart_disease'
    )
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    cp = models.IntegerField()  # Chest pain type
    trestbps = models.IntegerField()  # Resting blood pressure
    chol = models.IntegerField()  # Serum cholesterol
    fbs = models.BooleanField()  # Fasting blood sugar > 120 mg/dl
    restecg = models.IntegerField()  # Resting electrocardiographic results
    thalach = models.IntegerField()  # Maximum heart rate achieved
    exang = models.BooleanField()  # Exercise-induced angina
    oldpeak = models.FloatField()  # ST depression induced by exercise
    slope = models.IntegerField()  # Slope of the peak exercise ST segment
    ca = models.IntegerField()  # Number of major vessels colored by fluoroscopy
    thal = models.IntegerField()  # Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect)
    prediction_result = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.name} - {self.prediction_result}"
