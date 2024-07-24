from django.db import models
from datetime import datetime, timedelta, date

class TaskDetails(models.Model):
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.IntegerField(default=5, blank=True, null=True)  
    category = models.CharField(default="Personal",max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
            unique_together = ('username', 'title', 'description')
