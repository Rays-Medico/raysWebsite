from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'schedule_time']
        widgets = {
            'schedule_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }