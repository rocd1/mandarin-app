from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ChapterViewSet,
    LessonViewSet,
    PostViewSet,
    CommentViewSet,
    LessonProgressViewSet,
)

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'progress', LessonProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

