from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")
    
    def mark_as_completed(self):
        self.completed = True
        self.save()

    def is_overdue(self):
        if self.due_date:
            return not self.completed and self.due_date < timezone.now().date()
        return False 

    class Meta:
        ordering = ['created_at','due_date']
        indexes = [
            models.Index(fields=['user', 'completed']),
        ]
