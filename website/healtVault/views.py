from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .forms import PDFForm, SimpleFileForm
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def upload_pdf(request):
    logger.info("=== Starting PDF upload view ===")
    logger.info(f"Default storage class: {default_storage.__class__.__name__}")
    
    if request.method == 'POST':
        logger.info("POST request received")
        form = PDFForm(request.POST, request.FILES)
        
        if form.is_valid():
            logger.info("Form is valid")
            
            # Don't save the model yet
            instance = form.save(commit=False)
            
            # Get the file from request.FILES
            file = request.FILES['pdf_file']
            title = form.cleaned_data['title']
            
            # Generate a unique filename
            filename = f"pdfs/{datetime.now().strftime('%Y/%m/%d')}/{file.name}"
            logger.info(f"Generated filename: {filename}")
            
            # Save directly to Azure
            azure_path = default_storage.save(filename, file)
            logger.info(f"File saved to Azure path: {azure_path}")
            
            # Update the model's file field
            instance.pdf_file.name = azure_path
            
            # Now save the model
            instance.save()
            logger.info(f"Model saved with file URL: {instance.pdf_file.url}")
            
            return redirect('healthVault:pdf_success')
        else:
            logger.info(f"Form errors: {form.errors}")
    else:
        form = PDFForm()
    
    return render(request, 'upload.html', {'form': form})