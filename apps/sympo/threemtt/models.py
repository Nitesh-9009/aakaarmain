from django.db import models

# Create your models here.
class threemtt(models.Model):
    email = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    year = models.CharField(max_length = 200)
    ref = models.CharField(max_length=100)
    colg = models.CharField(max_length = 200)
    def __str__(self):
        return (
            f"{self.name}"
        )
