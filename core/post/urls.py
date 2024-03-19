from django.urls import path
from .views import PostListView, PostDetailView, PostCreate, PostEdit, PostUpdate, PostDelete, PostReaction, PostComment, PostCommentDelete

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>/', PostDetailView.as_view(), name="detail"),
    path('create/', PostCreate.as_view(), name='create'),
    path('edit/', PostEdit.as_view(), name='edit'),
    path('update/', PostUpdate.as_view(), name='update'),
    path('delete/', PostDelete.as_view(), name='delete'),
    path('reaction/', PostReaction.as_view(), name='reaction'),
    path('comment/', PostComment.as_view(), name='comment'),
    path('comment/delete', PostCommentDelete.as_view(), name='comment_delete')
]
