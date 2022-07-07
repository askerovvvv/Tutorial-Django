from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from lesson.views import *

router = DefaultRouter()
# router.register('', LessonViewSet)

# router = SimpleRouter()
router.register('lesson', LessonViewSet)
router.register('adviser', AdviserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(router.urls))
]