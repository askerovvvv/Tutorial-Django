from django.urls import path, include
from rest_framework.routers import DefaultRouter

from course.views import *

router = DefaultRouter()
router.register('review', ReviewViewSet)
router.register('', CourseViewSet)


urlpatterns = [
    path('', include(router.urls))
]
