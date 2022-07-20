from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from lesson.views import *

router = DefaultRouter()

app_name = 'lesson'

router.register('adviser', AdviserViewSet)
# router.register('group', GroupLessonViewSet)

router.register('', LessonViewSet)

urlpatterns = [
    path('', include(router.urls), 'dw'),

]