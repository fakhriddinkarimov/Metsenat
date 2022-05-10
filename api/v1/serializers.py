from rest_framework import serializers
from db.models import *
from .validators import validate_positive
from .services import *

from django.db.models.functions import Coalesce
from django.db.models import Sum, Count


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    used_money = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = 'id', 'first_name', 'last_name', 'sponsor_status', 'company', 'money', 'used_money', 'status', 'email', 'created_dt'
        # fields = '__all__'
        extra_kwargs = {
            'money': {'allow_null': False, 'required': True, 'validators': [validate_positive]},
        }

    def create(self, validate_data):
        validate_data['status'] = 'Yangi'
        sponsor = Sponsor.objects.create(**validate_data)
        return sponsor

    @staticmethod
    def get_used_money(sponsor):
        used_money = sponsor.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return used_money

    def validate_company_name(self, value):
        if self.initial_data.get('sponsor_status') == 'Jsh':
            return value
        else:
            return None


class StudentSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    gained_money = serializers.SerializerMethodField()


    class Meta:
        model = Student
        fields = ['id', 'first_name', 'phone_number', 'contract', 'gained_money', 'degree', 'university',
                  'university_id']

        extra_kwargs = {
            'contract': {'allow_null': False, 'required': True, 'validators': [validate_positive]},
        }

    @staticmethod
    def get_gained_money(student):
        gained_money = student.sponsorships.aggregate(money_sum=Coalesce(Sum('money'), 0))['money_sum']
        return gained_money


class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = SponsorShip
        fields = ['id', 'student', 'student_id', 'sponsor', 'sponsor_id', 'money', ]
        extra_kwargs = {'money': {'allow_null': False, 'required': True, 'validators': [validate_positive]}}

    def update(self, instance, validated_data):
        instance = services_sponsorship_money_update(instance, validated_data)
        return instance

    def create(self, validated_data):
        instance = services_sponsorship_money_create(validated_data)
        return instance


class Sponsorship_Student_Serializer(serializers.ModelSerializer):
    sponsor = serializers.SerializerMethodField()

    class Meta:
        model = SponsorShip
        fields = ['id', 'sponsor', 'money']

    @staticmethod
    def get_sponsor(sponsorship):
        data = {
            'id': sponsorship.sponsor.id,
            'first_name': sponsorship.sponsor.first_name,
            'last_name': sponsorship.sponsor.last_name
        }
        return data


class Sponsorship_Sponsor_Serializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = SponsorShip
        fields = ['id', 'student', 'money']

    @staticmethod
    def get_student(sponsorship):
        data = {
            'id': sponsorship.student.id,
            'first_name': sponsorship.student.first_name,
            'last_name': sponsorship.student.last_name
        }
        return data


class Dashboard:
    def __init__(self):
        self.sponsored_money = SponsorShip.objects.aggregate(Sum('money'))['money__sum']
        self.contract_money = Student.objects.aggregate(Sum('contract'))['contract__sum']
        self.money = self.contract_money - self.sponsored_money

    @property
    def data(self):
        return self.__dict__


class DashboardStats:
    def __init__(self):
        self.sponsors_statistics = Sponsor.objects.extra({'created_dt': "date(created_dt)"}).values(
            'created_dt').annotate(
            count=Count('id')).values_list('created_dt', 'count')
        self.students_statistics = Student.objects.extra({'created_dt': "date(created_dt)"}).values(
            'created_dt', ).annotate(
            count=Count('id')).values_list('created_dt', 'count')

    @property
    def data(self):
        return self.__dict__
