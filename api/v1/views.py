from django.db.models import Sum
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import  IsAuthenticated,IsAdminUser,AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .pagination import CustomPagination
from .serializers import SponsorSerializer,UniversitySerializer,StudentSerializer,SponsorshipSerializer,Sponsorship_Student_Serializer,Sponsorship_Sponsor_Serializer,Dashboard,DashboardStats
from db.models import Sponsor,Student,University,SponsorShip

class Sponsor_list(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name','last_name' 'company_name']
    filterset_fields = ['money', 'status']

class Sponsor_detail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

class Student_list(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filterset_fields = ['degree', 'university', 'course']



class Student_detail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SponsorShip_list(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = SponsorShip.objects.all()
    serializer_class = SponsorshipSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['sponsor__first_name', 'sponsor__last_name', 'sponsor__company','student__first_name','student__last_name']
    filterset_fields = ['money']

class SponsorShip_detail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = SponsorShip.objects.all()
    serializer_class = SponsorshipSerializer

class University_list(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class University_detail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class Sponsorships_Student(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    serializer_class = Sponsorship_Student_Serializer

    def get_queryset(self):
        student = get_object_or_404(Student, id=self.kwargs['pk'])
        queryset = student.sponsorships.all()
        return queryset


class Sponsorships_Sponsor(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = Sponsorship_Sponsor_Serializer

    def get_queryset(self):
        sponsor = get_object_or_404(Sponsor, id=self.kwargs['pk'])
        queryset = sponsor.sponsorships.all()
        return queryset



class DashboardView(APIView):
     permission_classes = [IsAdminUser]

     @staticmethod
     def get(request, *args, **kwargs):
         dashboard_serializer = Dashboard()
         dashboard_stats_serializer = DashboardStats()
         return Response(data={
             'money_stat': dashboard_serializer.data,
             'dash_stats': dashboard_stats_serializer.data
         }
         )

class Dashboard(APIView):
     permission_classes = [IsAdminUser]

     def get(self, request, *args, **kwargs):
         all_payed_money = SponsorShip.objects.aggregate(Sum('money'))['money__sum']
         all_contract = Student.objects.aggregate(Sum('contract'))['contract__sum']
         data = {
             'all_payed_money': all_payed_money,
             'all_contract': all_contract,
             'all_rest': all_contract - all_payed_money,
         }
         return Response(data=data)
