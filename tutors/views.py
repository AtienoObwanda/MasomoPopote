import re
from typing import List
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.views.generic import DeleteView, ListView, UpdateView,DetailView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .models import *
from .forms import *

class TutorReg(CreateView):
    model = User
    form_class = TutorRegisterForm
    template_name = 'tutors/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('tutor-login')


def loginTutor(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('tutor')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'tutors/login.html',
    context={'form':AuthenticationForm()})


def tutor(request):

    publishedCourses = Course.objects.filter(tutor = request.user.tutor).all()
    # enroll = StudentProfile.enrolledIn
    # students = publishedCourses.students.all()

    students = Student.objects.filter(enrolls__id__in = publishedCourses).all()
    # instance = Student.objects.filter(enrolls__id__in = publishedCourses).values('user')[0]
    print(students)
    count = students.count()
    print(count)
    return render(request, 'tutors/tutor.html', {'publishedCourses': publishedCourses, 'students': students, 'count': count})

def publishedTests(request):
        publishedTests = test.objects.all()

        return render(request, 'tutors/postedTest.html', {'publishedTests': publishedTests})


class addCourse(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title','category','coursePoster', 'descriptions', 'body']
    template_name = 'tutors/newCourse.html'
    def form_valid(self, form):
        form.instance.tutor=self.request.user.tutor
        return super().form_valid(form)

class addTest(LoginRequiredMixin, CreateView):
    model = test
    fields = ['title','course', 'body']
    template_name = 'tutors/newTest.html'
    def form_valid(self, form):
        # form.instance.tutor=self.request.user
        return super().form_valid(form)


    
   
