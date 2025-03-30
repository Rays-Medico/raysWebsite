from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'timetable/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_tasks'] = self.get_queryset().filter(status='pending')
        context['completed_tasks'] = self.get_queryset().filter(status='completed')
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'timetable/task_detail.html'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'timetable/task_form.html'
    success_url = reverse_lazy('timetable:task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'timetable/task_form.html'
    success_url = reverse_lazy('timetable:task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'timetable/task_confirm_delete.html'
    success_url = reverse_lazy('timetable:task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# @login_required
def mark_task_completed(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.save()
    messages.success(request, f'Task "{task.name}" marked as completed!')
    return redirect('timetable:task_list')

# @login_required
def mark_task_pending(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'pending'
    task.save()
    messages.success(request, f'Task "{task.name}" marked as pending!')
    return redirect('timetable:task_list')