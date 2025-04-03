from django.contrib import admin
from django.urls import path
from studentorg.views import HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView
from studentorg.views import OrgMemberListView, OrgMemberCreateView, OrgMemberUpdateView, OrgMemberDeleteView
from studentorg.views import StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView
from studentorg.views import CollegeListView, CollegeCreateView, CollegeUpdateView, CollegeDeleteView
from studentorg import views
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth

from django.db.models import Count
from datetime import datetime

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),
    path('orgmember_list/', OrgMemberListView.as_view(), name='orgmember-list'),
    path('orgmember_list/add', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<pk>', OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<pk>/delete/', OrgMemberDeleteView.as_view(), name='orgmember-delete'),
    path('student_list/', StudentListView.as_view(), name='student-list'),
    path('student_list/add/', StudentCreateView.as_view(), name='student-add'),
    path('student_list/<pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
    path('college_list/', CollegeListView.as_view(), name='college-list'),
    path('college_list/add/', CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>/', CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete/', CollegeDeleteView.as_view(), name='college-delete'),
]
