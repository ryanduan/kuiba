from django.db import models
from django.utils import timezone
import datetime

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question
