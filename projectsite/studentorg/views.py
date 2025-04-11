from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from .models import Organization, OrgMember, Student, College, Program
from .forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.views.generic.list import ListView
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from datetime import datetime, timedelta
from django.db import connection


@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass
    
def orgMemDoughnutChart(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT o.name, COUNT(om.id) AS member_count
                FROM studentorg_organization o
                LEFT JOIN studentorg_orgmember om ON o.id = om.organization_id
                GROUP BY o.name
            """)
            rows = cursor.fetchall()
        
        result = {name: count for name, count in rows if name}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def studentCountEveryCollege(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.college_name, COUNT(s.id) AS student_count
                FROM studentorg_college c
                LEFT JOIN studentorg_program p ON c.id = p.college_id
                LEFT JOIN studentorg_student s ON p.id = s.program_id
                GROUP BY c.college_name
            """)
            rows = cursor.fetchall()
        
        result = {name: count for name, count in rows if name}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def radarStudenCountEveryCollege(request):
    try:
        # Reuse the same data as studentCountEveryCollege
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.college_name, COUNT(s.id) AS student_count
                FROM studentorg_college c
                LEFT JOIN studentorg_program p ON c.id = p.college_id
                LEFT JOIN studentorg_student s ON p.id = s.program_id
                GROUP BY c.college_name
            """)
            rows = cursor.fetchall()
        
        result = {name: count for name, count in rows if name}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def programPolarchart(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.prog_name, COUNT(s.id) AS student_count
                FROM studentorg_program p
                LEFT JOIN studentorg_student s ON p.id = s.program_id
                GROUP BY p.prog_name
            """)
            rows = cursor.fetchall()
        
        result = {name: count for name, count in rows if name}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def htmlLegendsChart(request):
    with connection.cursor() as cursor:
        # Execute raw SQL query to count student members for each organization and their month joined
        cursor.execute("""
            SELECT studentorg_organization.name, COUNT(studentorg_orgmember.id) AS student_count, STRFTIME('%m', studentorg_orgmember.date_joined) AS joined_month
            FROM studentorg_orgmember
            INNER JOIN studentorg_organization ON studentorg_orgmember.organization_id = studentorg_organization.id
            GROUP BY studentorg_organization.name, joined_month
        """)
        # Fetch all rows from the cursor
        rows = cursor.fetchall()
        
    # Prepare data for the chart
    result = {}
    for org_name, count, joined_month in rows:
        if org_name not in result:
            result[org_name] = {'student_count': {}, 'total_students': 0}
        result[org_name]['student_count'][joined_month] = count
        result[org_name]['total_students'] += count

    return JsonResponse(result)



class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(college__college_name__icontains=query) | Q(description__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class OrgMemberListView(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(student__lastname__icontains=query), 
                Q(student__firstname__icontains=query), 
                Q(organization__name__icontains=query),  
            )
        return qs
    
class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_delete.html'
    success_url = reverse_lazy('orgmember-list')

class StudentListView(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(lastname__icontains=query),    
                Q(firstname__icontains=query),    
            )
        return qs
    
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('student-list')

class CollegeListView(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(college_name__icontains=query)  # Look for college name
            )
        return qs
    
class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_delete.html'
    success_url = reverse_lazy('college-list')

class ProgramListView(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program_list.html'
    paginate_by = 5
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(prog_name__icontains=query)  # Look for program name
            )
        return qs
    
class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_delete.html'
    success_url = reverse_lazy('program-list')