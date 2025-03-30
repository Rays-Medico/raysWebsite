from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from timetable.models import Task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send notifications for tasks that are due soon'

    def add_arguments(self, parser):
        parser.add_argument('--minutes', type=int, default=15,
                            help='Number of minutes before a task is due to send a notification')

    def handle(self, *args, **options):
        minutes = options['minutes']
        self.stdout.write(f'Checking for tasks due in the next {minutes} minutes...')
        
        now = timezone.now()
        soon_time = now + timezone.timedelta(minutes=minutes)
        
        # Find pending tasks that are due within the specified time window and 
        # haven't had notifications sent yet
        tasks = Task.objects.filter(
            status='pending',
            notification_sent=False,
            schedule_time__gt=now,
            schedule_time__lte=soon_time
        )
        
        count = 0
        for task in tasks:
            self.send_notification(task)
            task.notification_sent = True
            task.save()
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully sent {count} notifications'))

    def send_notification(self, task):
        """Send notification about the task"""
        user = task.user
        if user.email:
            try:
                subject = f'Reminder: {task.name} is due soon'
                message = f"""
                Hello {user.username},
                
                This is a reminder that your task "{task.name}" is due at {task.schedule_time.strftime('%Y-%m-%d %H:%M')}.
                
                Description: {task.description}
                
                Thank you,
                Your Timetable App
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                
                self.stdout.write(f'Sent notification email for task {task.id} to {user.email}')
                
            except Exception as e:
                logger.error(f"Failed to send notification for task {task.id}: {e}")
        else:
            logger.warning(f"User {user.id} has no email address, can't send notification for task {task.id}")

