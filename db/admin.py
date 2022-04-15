from django.contrib import admin
from .models import Sponsor,Student,SponsorShip,Univer
# Register your models here.

admin.site.register(Sponsor)
admin.site.register(Student)
admin.site.register(Univer)
admin.site.register(SponsorShip)

