from django.db import models

# Create your models here.


class Submission(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    colgName = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    mobileNo = models.IntegerField()
    emails = models.CharField(max_length=100, default="email@y.com")
    program = models.CharField(max_length=100)
    year = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    ref = models.CharField(max_length=100)


    def __str__(self):
        return (
            f"{self.name} | "
            f"{self.email} |"
            f"{self.emails}"
        )


class Seismic(models.Model):
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
    category = models.CharField(max_length=10)
    ref = models.CharField(max_length=100)
    
    def __str__(self):
        return (
            f"{self.team}"
        )





class BridgeIt(models.Model):
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

class ConquerIt(models.Model):
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

