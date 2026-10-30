from django.db import models

# Create your models here.

class ceohour(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=100)
    org = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Cenex(models.Model):
    team = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    name1 = models.CharField(max_length=50)
    email1 = models.CharField(max_length=200)
    contact1 = models.IntegerField()
    colg1 = models.CharField(max_length = 200)
    name2 = models.CharField(max_length=50)
    email2 = models.CharField(max_length=200)
    contact2 = models.CharField(max_length=15)
    colg2 = models.CharField(max_length = 200)
    name3 = models.CharField(max_length=50)
    email3 = models.CharField(max_length=200)
    contact3 = models.CharField(max_length=15)
    colg3 = models.CharField(max_length = 200)
    name4 = models.CharField(max_length=50)
    email4 = models.CharField(max_length=200)
    contact4 = models.CharField(max_length=15)
    colg4 = models.CharField(max_length = 200)
    ref = models.CharField(max_length=100)
    
    def __str__(self):
        return (
            f"{self.team}"
        )
    

class StaadPro(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    colg = models.CharField(max_length = 200)
    
    def __str__(self):
        return (
            f"{self.name}"
        )
        
        

class Fusion(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    colg = models.CharField(max_length = 200)
    
    def __str__(self):
        return (
            f"{self.name}"
        )
class LabVisit(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    colg = models.CharField(max_length = 200)
    ref = models.CharField(max_length=100)
    def __str__(self):
        return (
            f"{self.name}"
        )

class Primavera(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    colg = models.CharField(max_length = 200)
    ref = models.CharField(max_length=100)
    def __str__(self):
        return (
            f"{self.name}"
        )

class Fusionplusstaad_reg(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    colg = models.CharField(max_length = 200)
    ref = models.CharField(max_length=100)
    def __str__(self):
        return (
            f"{self.name}"
        )





class Primavera_payment(models.Model):
    email = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='primavera_photos/')
    def __str__(self):
        return (
            f"{self.email}"
        )
class Fusion_payment(models.Model):
    email = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='fusion_photos/')
    def __str__(self):
        return (
            f"{self.email}"
        )
class Staad_payment(models.Model):
    email = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='staad_photos/')
    def __str__(self):
        return (
            f"{self.email}"
        )
class Fusionplusstaad_payment(models.Model):
    email = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='fusionplusstaad_photos/')
    def __str__(self):
        return (
            f"{self.email}"
        )
class Primaveraplusstaad_payment(models.Model):
    email = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='primaveraplusstaad_photos/')
    def __str__(self):
        return (
            f"{self.email}"
        )
class labpayment_modal(models.Model):
    email = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='primaveraplusstaad_photos/')
    def __str__(self):
        return (
            f"{self.email}"
        )
