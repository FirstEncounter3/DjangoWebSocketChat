# chat/urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('signup/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('api/', include(router.urls), name='api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += router.urls
