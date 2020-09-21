from django.shortcuts import render
# from Diary.forms import 
# from Diary.models import 
from datetime import datetime
from django.http import HttpResponse
from django.views.generic.edit import FormView
from Diary.forms import UserCreationForm
from django.views.generic.base import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "login"
    template_name = "registration/register.html"
    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")



