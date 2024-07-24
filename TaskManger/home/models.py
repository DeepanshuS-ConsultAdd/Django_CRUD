from django.db import models

class TaskDetails(models.Model):
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.IntegerField(default=5)  
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

