from django import forms
from .models import PDFDocument,SimpleFileTest

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'pdf_file']

class SimpleFileForm(forms.ModelForm):
    class Meta:
        model = SimpleFileTest
        fields = ['file']