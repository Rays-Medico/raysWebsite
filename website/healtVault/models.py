from django.db import models

# Create your models here.
class PDFDocument(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/%Y/%m/%d/')  # Path in Azure container
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class SimpleFileTest(models.Model):
    file = models.FileField(upload_to='test/')