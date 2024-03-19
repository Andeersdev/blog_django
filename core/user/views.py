from django.shortcuts import render
from core.user.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


class Register(CreateView):
    model = User
    template_name = 'user/register.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('')
