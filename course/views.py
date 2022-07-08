from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from course.models import *
from course.serializers import *


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'rating']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAdminUser]

        return [permission() for permission in permissions]

    # @action(methods=['POST'], detail=True)
    # def rating(self, request, pk):
    #     serializer = RatingSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     try:
    #         obj = Review.objects.get(course=self.get_object(), user=request.user)
    #         obj.rating = request.data['rating']
    #     except Review.DoesNotExist:
    #         obj = Review(user=request.user, course=self.get_object(), rating=request.data['rating'])
    #
    #     obj.save()
    #     return Response(request.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        course = self.get_object()
        like_obj, _ = Like.objects.get_or_create(course=course, user=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'Liked'
        if not like_obj.like:
            status = 'Unliked'
        return Response({'status': status})






