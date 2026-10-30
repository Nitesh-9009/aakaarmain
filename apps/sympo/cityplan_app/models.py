
from django.db import models


class cityplan_reg(models.Model):


    
    participant1 = models.CharField(max_length=200)
    email1 = models.CharField(max_length=100)
    contact1 = models.CharField(max_length=12)
    participant2 = models.CharField(max_length=200)
    email2 = models.CharField(max_length=100)
    contact2 = models.CharField(max_length=12)
    participant3 = models.CharField(max_length=200)
    email3 = models.CharField(max_length=100)
    contact3 = models.CharField(max_length=12)
    participant4 = models.CharField(max_length=200)
    email4 = models.CharField(max_length=100)
    contact4 = models.CharField(max_length=12)
    ref = models.CharField(max_length=50)
    

    def __str__(self):
        return (
            f"{self.participant1} | "
            f"{self.email1} "
        )

from django.db import models

# Create your models here.
