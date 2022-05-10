from django.urls import path
from .views import *


urlpatterns = [
    path('sponsor',Sponsor_list.as_view(),name='sponsor-list'),
    path('sponsor/<int:pk>', Sponsor_detail.as_view(), name='sponsor'),
    path('sponsor/<int:pk>/sponsorships', Sponsorships_Sponsor.as_view(), name='sponsor-sponsorships'),

    path('students', Student_list.as_view(), name='student-list'),
    path('students/<int:pk>', Student_detail.as_view(), name='student'),
    path('students/<int:pk>/sponsorships', Sponsorships_Student.as_view(), name='student-sponsorships'),

    path('sponsorship', SponsorShip_list.as_view(), name='sponsorship-list'),
    path('sponsorship/<int:pk>', SponsorShip_detail.as_view(), name='sponsorship'),
    path('university',University_list.as_view(),name='university-list'),
    path('university/<int:pk>',University_detail.as_view(),name='university'),

    path('dashboard', DashboardView.as_view(), name='dashboard'),
    #path('dash',Dashboard.as_view(),name='dash')

]

