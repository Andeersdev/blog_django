from django.shortcuts import render
from django.views.generic import TemplateView
from core.post.models import Post, Reactions, Comments
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        # (id) -> los primero (-id) -> los ultimos [:n] -> cantidad de registros
        context['count_post'] = Post.objects.filter(user=user).count()
        # Instancio los post del usuario actual
        user_post = Post.objects.filter(user=user)
        print(user_post)
        context['count_like'] = Reactions.objects.filter(
            post__in=user_post).count()
        context['count_comment'] = Comments.objects.filter(
            post__in=user_post).count()
        context['posts'] = Post.objects.filter(
            user=self.request.user).order_by('-id')[:3]
        return context
