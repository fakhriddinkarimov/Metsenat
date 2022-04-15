from re import M, T
from statistics import mode
from django.db import models

# Create your models here.

class Sponsor(models.Model):
    Status = (
        ('Yangi', 'Yangi'),
        ('Moderatsiya','Moderatsiya'),
        ('Tasdiqlangan','Tasdiqlangan')
        ('Bekor qilingan','Bekor qilingan')
    )

    Sponsor_Status(
        ('Jsh','Jismoniy shaxs'),
        ('Ysh','Yuridik shaxs')
    )

    first_name = models.CharField(max_length=32,blank=False,null=False)
    last_name = models.CharField(max_length=32,blank=False,null=False)
    SponsorStatus = models.CharField(max_length=24,choices=SponsorStatus,default='Jsh',null=False,blank=False)
    company = models.CharField(max_length=64,null=True)
    money = models.IntegerField(null=False,blank=False)
    status = models.CharField(max_length=32,choices=Status,default='Yangi')
    email = models.CharField(max_length=64,blank=False,null=False)
    crated_dt = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name}   {self.last_name}"


class Univer(models.Model):
    name = models.CharField(max_length=128,blank=False,null=False)

    def __str__(self):
        return self.name


class Student(models.Model):
    Degree = (
        ('Bakalavr','Bakalavr'),
        ('Magistr','Magistr'),
    )

    first_name = models.CharField(max_length=32,blank=False,null=False)
    last_name = models.CharField(max_length=32,blank=False,null=False)
    unversity = models.ForeignKey(Univer,on_delete=models.CASCADE)
    degree = models.CharField(max_length=32,blank=False,null=False)
    contract =models.IntegerField(null=False)
    phone_number = models.CharField(max_length=14,null=False,blank=False)
    email = models.CharField(max_length=64,blank=False,null=False)
    created_dt = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name}  {self.last_name}"



class SponsorShip(models.Model):
    sponsor = models.ForeignKey(Sponsor,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    money = models.IntegerField(null=False,blank=False)
    created_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.sponsor.last_name} {self.sponsor.last_name} -- {self.student.first_name} {self.student.last_name}"
        