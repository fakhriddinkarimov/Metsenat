from db.models import *
from rest_framework.generics import get_object_or_404
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.validators import ValidationError

def services_sponsorship_money_update(instance,validate_data):
    student = instance.student
    sponsor = get_object_or_404(Sponsor,id=validate_data['sponsor_id'])
    money = validate_data['money']

    student_money = student.sponsorship.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money',0)))['money_sum']
    sponsor_money = sponsor.sponsorship.exclude(id=instance.id).aggregate(money_sum=Coalesce(Sum('money'),0))['money_sum']
    sum_money = sponsor.money - sponsor_money
    if money <= sum_money:
        if student_money + money <= student.contract:
            instance.money = money
            instance.sponsor = sponsor
            instance.save()
            return instance
        else:
            raise ValidationError({'money': 'Homiylik puli kontrakt miqdordan kop'})
    else:
        raise ValidationError({'money': 'Homiyda yetarli mablag mavjud emas'})

def services_sponsorship_money_create(validated_data):
    sponsor = get_object_or_404(Sponsor,id=validated_data.get('sponsor_id'))
    student = get_object_or_404(Student,id=validated_data.get('student_id'))
    money = validated_data.get('money')


    sponsor_money  = sponsor.sponsorships.aggregate(money_sum=Coalesce(Sum('money'),0))['money_sum']
    student_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'),0))['money_sum']
    sum_money = sponsor.money - sponsor_money

    if money <= sum_money:
        if student_money + money <= student.contract:
            sponsorship = SponsorShip.objects.create(**validated_data)
            return sponsorship
        else:
            raise ValidationError({'money': 'Homiylik puli kontraktdan oshib ketti'})
    else:
        raise ValidationError({'money': 'Homiyda yetarli pul mavjud emas'})
