
from django.contrib import admin
from django.urls import path, include
from .views import LoginView, RegisterCreateView, Logout, HomeView, AboutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('dashboard/', include('core.dashboard.urls')),
    path('post/', include('core.post.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
