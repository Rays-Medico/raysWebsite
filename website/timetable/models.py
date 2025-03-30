# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone


# class Task(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     schedule_time = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     notification_sent = models.BooleanField(default=False)


from django.db import models
from django.conf import settings  # Add this import
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Change this line
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notification_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['schedule_time']
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()}) - {self.schedule_time.strftime('%Y-%m-%d %H:%M')}"
    
    def is_due_soon(self, minutes=15):
        """Check if the task is due within the specified number of minutes"""
        now = timezone.now()
        time_difference = self.schedule_time - now
        return time_difference.total_seconds() <= minutes * 60 and time_difference.total_seconds() > 0
    
    def is_overdue(self):
        """Check if the task is overdue"""
        return timezone.now() > self.schedule_time and self.status == 'pending'
