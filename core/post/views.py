import json
import os
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DetailView
from .models import Post, Reactions, Comments
from .forms import PostForm
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post/post.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = PostForm
        return context

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(user=user)
        return posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # instancia del objecto actual
        post = self.object
        context['comments'] = Comments.objects.filter(post=post)
        return context


class PostCreate(LoginRequiredMixin, View):
    def post(self, request):
        try:
            title = request.POST['title']
            content = request.POST['content']
            image = request.FILES['image']
            post = Post.objects.create(
                title=title, content=content, image=image, user=request.user)
            return JsonResponse({'message': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'mal'}, status=400)


class PostEdit(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            id = data['id']
            post = Post.objects.get(id=id)
            data_json = model_to_dict(post)
            data_json['image'] = post.image.url if post.image else None
            return JsonResponse({'data': data_json}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'mal'}, status=400)


class PostUpdate(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST['id']
            title = request.POST['title']
            content = request.POST['content']
            post_found = Post.objects.get(id=id)
            if 'image' in request.FILES:
                image = request.FILES['image']
                if post_found.image is not None:
                    old_image_path = post_found.image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
            else:
                image = post_found.image

            if (post_found is not None):
                post_found.title = title
                post_found.content = content
                post_found.image = image
                post_found.save()
            return JsonResponse({'message': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'mal'}, status=400)


class PostDelete(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            id = data['id']
            post = Post.objects.get(id=id)
            post.delete()
            return JsonResponse({'message': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'Error'}, status=400)


class PostReaction(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                post_id = data['postId']
                user = request.user
                post = Post.objects.get(id=post_id)
                # Retorna un bool si el filtro existe o no
                user_has_reaction = Reactions.objects.filter(
                    user=user, post=post).exists()
                if user_has_reaction:
                    # El usuario ya ha reaccionado, eliminamos la reacción
                    found_user_reaction = Reactions.objects.get(
                        user=user, post=post)
                    found_user_reaction.delete()
                else:
                    reaction = Reactions.objects.create(
                        post=post, user=user, likes=1)
                return JsonResponse({'data': True}, status=200)
            except Exception as e:
                return JsonResponse({'data': str(e)}, status=400)
        else:
            return JsonResponse({'data': 'Please, Sign in!'}, status=401)


class PostComment(LoginRequiredMixin, View):
    def post(self, request):
        try:
            user = request.user
            post_id = request.POST['id']
            comment = request.POST['comment']
            post = Post.objects.get(id=post_id)
            new_comment = Comments.objects.create(
                user=user, post=post, comment=comment)
            return JsonResponse({'data': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'data': str(e)}, status=400)


class PostCommentDelete(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data['commentId']
            comment = Comments.objects.get(id=comment_id)
            comment.delete()
            return JsonResponse({'data': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'data': str(e)}, status=400)
