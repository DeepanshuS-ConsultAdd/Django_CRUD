from django.db import models

class TaskDetails(models.Model):
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=False, null=False)
    due_date = models.DateField(blank=False, null=False)
    priority = models.IntegerField(default=5)  
    category = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.title

