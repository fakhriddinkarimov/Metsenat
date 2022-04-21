from django.contrib import admin
from .models import Sponsor,Student,SponsorShip,University
# Register your models here.

admin.site.register(Sponsor)
admin.site.register(Student)
admin.site.register(University)
admin.site.register(SponsorShip)

