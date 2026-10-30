from django.db import models

# Create your models here.


class Submission(models.Model):
    author = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    colgName = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    mobileNo = models.IntegerField()
    co1 = models.CharField(max_length=200)
    mail1 = models.CharField(max_length=100)
    co2 = models.CharField(max_length=200)
    mail2 = models.CharField(max_length=100)
    co3 = models.CharField(max_length=200)
    mail3 = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    others = models.CharField(max_length=100)
    abstract = models.FileField(upload_to='doc/')
    authentication = models.FileField(upload_to='doc/')
    referral = models.CharField(max_length=100)
    def __str__(self):
        return (
            f"{self.author} | "
            f"{self.email} "
        )

class iitb(models.Model):
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    ldap = models.CharField(max_length = 200)
    roll = models.CharField(max_length=200)
    department=models.CharField(max_length=200)  
    def __str__(self):
        return (
            f"{self.name}"
        )
class non_iitb(models.Model):
    name= models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    college = models.CharField(max_length=200)
    transaction_id=models.IntegerField()
    payment_screenshot=models.ImageField(upload_to='payment_screenshot/')
   
    def __str__(self):
        return (
            f"{self.name} | "
            f"{self.college} "
        )
