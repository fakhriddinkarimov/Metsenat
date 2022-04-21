from re import M, T
from statistics import mode
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Sponsor(models.Model):
    status_choices = (
        ('Yangi', 'Yangi'),
        ('Moderatsiya','Moderatsiya'),
        ('Tasdiqlangan','Tasdiqlangan'),
        ('Bekor qilingan','Bekor qilingan')
    )

    sponsor_choices = (
        ('Jsh','Jismoniy shaxs'),
        ('Ysh','Yuridik shaxs')
    )

    first_name = models.CharField(max_length=32,blank=False,null=False)
    last_name = models.CharField(max_length=32,blank=False,null=False)
    sponsor_status = models.CharField(max_length=24,choices=sponsor_choices,default='Jsh')
    company = models.CharField(max_length=64,null=True)
    money = models.IntegerField(null=False,blank=False)
    status = models.CharField(max_length=32,choices=status_choices,default='Yangi')
    email = models.CharField(max_length=64,blank=False,null=False)
    created_dt = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name}   {self.last_name}"


class University(models.Model):
    name = models.CharField(max_length=128,blank=False,null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'


class Student(models.Model):
    degree_choices = (
        ('Bakalavr','Bakalavr'),
        ('Magistr','Magistr'),
    )

    first_name = models.CharField(max_length=32,blank=False,null=False)
    last_name = models.CharField(max_length=32,blank=False,null=False)
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    degree = models.CharField(max_length=32,choices=degree_choices,default='Bakalavr', blank=False)
    course = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(4)])
    contract = models.IntegerField(null=False)
    phone_number = models.CharField(max_length=14,null=False,blank=False)
    email = models.CharField(max_length=64,blank=False,null=False)
    created_dt = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name}  {self.last_name}"



class SponsorShip(models.Model):
    sponsor = models.ForeignKey(Sponsor,related_name='sponsorships',on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name='sponsorships',on_delete=models.CASCADE)
    money = models.IntegerField(null=False,blank=False)
    created_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"Sponsor :{self.sponsor.last_name} {self.sponsor.last_name} -> Student {self.student.first_name} {self.student.last_name}"

    class Meta:
        verbose_name = 'Sponsorship'
        verbose_name_plural = 'Sponsorships'