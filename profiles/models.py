from django.db import models
from datetime import datetime
# Create your models here.

class Profiles(models.Model):
    # Entries enter here maybe like the column queries
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now, blank=True)