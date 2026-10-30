from django.db import models

# Create your models here.


class poster_class(models.Model):
    email = models.CharField(max_length=200)
    name1 = models.CharField(max_length=50)
    mail1 = models.CharField(max_length=200)
    mobile1 = models.CharField(max_length=25)
    college = models.CharField(max_length=200)
    name2 = models.CharField(max_length=50)
    mail2 = models.CharField(max_length=200)
    mobile2 = models.CharField(max_length=25)
    name3 = models.CharField(max_length=50)
    mail3 = models.CharField(max_length=200)
    mobile3 = models.CharField(max_length=25)
    mail3 = models.CharField(max_length=200)
    field = models.CharField(max_length=100)
#    title = models.CharField(max_length=200)
    others = models.CharField(max_length=100)
    ref=models.CharField(max_length=100)
    experience=models.CharField(max_length=1000)    
    def __str__(self):
        return (
            f"{self.name1}  "
            
        )
