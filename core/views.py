from django.shortcuts import render, HttpResponseRedirect
from core.user.models import User
from django.views.generic import View, TemplateView, CreateView
from core.user.forms import UserRegisterForm
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.conf import settings
from core.post.models import Post, Reactions, Comments
from django.db.models import Sum, Count
from django.contrib import messages
from django.db import connection


class LoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('dashboard:index'))
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'Credentials do not match!')
        return super().form_invalid(form)


class RegisterCreateView(CreateView):
    model = User
    template_name = 'auth/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy(settings.LOGOUT_REDIRECT_URL))


def get_all_post_r_c():
    with connection.cursor() as cursor:
        cursor.callproc('get_all_post_r_c')
        resultados = cursor.fetchall()
        return resultados


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_all_post_r_c()
        return context


class AboutView(TemplateView):
    template_name = 'home/about.html'
