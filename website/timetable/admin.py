from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'schedule_time', 'status', 'notification_sent')
    list_filter = ('status', 'notification_sent', 'schedule_time')
    search_fields = ('name', 'description', 'user__username')
    date_hierarchy = 'schedule_time'