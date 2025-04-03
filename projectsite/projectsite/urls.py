from django.contrib import admin
from django.urls import path
from studentorg.views import HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView
from studentorg.views import OrgMemberListView, OrgMemberCreateView, OrgMemberUpdateView
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
]
