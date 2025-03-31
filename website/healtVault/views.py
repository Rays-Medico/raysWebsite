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
            filename = f"{file.name}"
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

import os
from datetime import datetime
from calendar import month_name
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_pdf_files(year=None, month=None, day=None, search=None):
    """Scan the file system for PDF files with the date structure"""
    # Define the base path to your pdfs folder
    pdfs_base_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    pdf_files = []
    
    # Check if directory exists
    if not os.path.exists(pdfs_base_dir) or not os.path.isdir(pdfs_base_dir):
        return pdf_files
        
    # Walk through the directory structure
    for root, dirs, files in os.walk(pdfs_base_dir):
        # Get the parts of the path to determine year/month/day
        rel_path = os.path.relpath(root, pdfs_base_dir)
        
        # Skip the base directory itself
        if rel_path == '.':
            continue
            
        parts = rel_path.split(os.sep)
        
        # Check if we have a valid date structure
        if len(parts) >= 3:
            try:
                file_year, file_month, file_day = parts[0], parts[1], parts[2]
                
                # Validate date components
                if not (file_year.isdigit() and file_month.isdigit() and file_day.isdigit()):
                    continue
                    
                # Filter by date if specified
                if year and year != file_year:
                    continue
                if month and month != file_month:
                    continue
                if day and day != file_day:
                    continue
                
                # Process PDF files in this directory
                for filename in files:
                    if not filename.lower().endswith('.pdf'):
                        continue
                        
                    # Filter by search term if specified
                    if search and search.lower() not in filename.lower():
                        continue
                        
                    file_path = os.path.join(root, filename)
                    
                    # Get file modified time
                    try:
                        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    except OSError:
                        modified_time = datetime.now()
                    
                    # Create relative path from MEDIA_ROOT for URL
                    rel_path_for_url = os.path.relpath(file_path, settings.MEDIA_ROOT)
                    file_url = f"{settings.MEDIA_URL}{rel_path_for_url.replace(os.sep, '/')}"
                    
                    # Format date string
                    date_str = f"{file_year}-{file_month.zfill(2)}-{file_day.zfill(2)}"
                    
                    pdf_files.append({
                        'name': filename,
                        'modified_time': modified_time,
                        'url': file_url,
                        'date_str': date_str,
                        'year': file_year,
                        'month': file_month,
                        'day': file_day
                    })
            except (ValueError, IndexError):
                # Skip directories with invalid structure
                continue
    
    # Sort files by date (newest first) and then by name
    pdf_files.sort(key=lambda x: (f"{x['year']}-{x['month'].zfill(2)}-{x['day'].zfill(2)}", x['name']), reverse=True)
    
    return pdf_files

def get_available_dates():
    """Get all available years, months, and days for filtering"""
    pdfs_base_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    years = set()
    months = set()
    days = set()
    
    if not os.path.exists(pdfs_base_dir) or not os.path.isdir(pdfs_base_dir):
        return years, months, days
        
    # Walk through year directories
    for item in os.listdir(pdfs_base_dir):
        year_path = os.path.join(pdfs_base_dir, item)
        if os.path.isdir(year_path) and item.isdigit():
            years.add(item)
            
            # Walk through month directories
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path) and month.isdigit():
                    months.add(month.zfill(2))
                    
                    # Walk through day directories
                    for day in os.listdir(month_path):
                        day_path = os.path.join(month_path, day)
                        if os.path.isdir(day_path) and day.isdigit():
                            days.add(day.zfill(2))
    
    return sorted(years, reverse=True), sorted(months), sorted(days)

def get_month_names(months):
    """Convert month numbers to month names"""
    return [(month, month_name[int(month)]) for month in months]

def build_query_params(params):
    """Build query string for pagination links"""
    filtered_params = {k: v for k, v in params.items() if k != 'page' and v}
    return '&'.join([f"{k}={v}" for k, v in filtered_params.items()])

def vault(request):
    """Main view function to display all PDF files without filtering by default"""
    # Get filter parameters (but don't use them by default)
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    day = request.GET.get('day', '')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    # Get all PDF files without applying filters by default
    pdf_files = get_pdf_files()
    
    # Paginate results
    paginator = Paginator(pdf_files, 10)  # 10 PDFs per page
    try:
        paginated_pdfs = paginator.page(page)
    except PageNotAnInteger:
        paginated_pdfs = paginator.page(1)
    except EmptyPage:
        paginated_pdfs = paginator.page(paginator.num_pages)
    
    # Get available filter options (keep these for potential future use)
    years, months, days = get_available_dates()
    months_with_names = get_month_names(months)
    
    # Build query params for pagination links
    query_params = build_query_params(request.GET.dict())
    
    # Prepare context data
    context = {
        'pdf_files': paginated_pdfs,
        'paginator': paginator,
        'years': years,
        'months': months_with_names,
        'days': days,
        'selected_year': year,
        'selected_month': month,
        'selected_day': day,
        'search_query': search_query,
        'search_active': False,  # Set to False to always show all files
        'query_params': query_params
    }
    
    return render(request, 'vault.html', context)