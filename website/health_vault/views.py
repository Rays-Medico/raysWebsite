from django.views import generic
from .models import Document
from .forms import DocumentForm

class DocumentList(generic.ListView):
    model = Document
    template_name = 'health_vault/index.html'

class DocumentCreate(generic.CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'health_vault/upload.html'
    success_url = '/health_vault/'

class DocumentDetail(generic.DetailView):
    model = Document
    template_name = 'health_vault/view.html'