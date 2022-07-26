import logging

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from course.models import *
from course.serializers import *

logger = logging.getLogger('')


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f'from ReviewViewSet -- {self.request.user}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'saved', 'like']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAdminUser]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
            SearchHistory.objects.create(user=self.request.user, item=search)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseRetrieveSerializer(instance)
        return Response(serializer.data)

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

    @action(methods=['POST'], detail=True)
    def saved(self, request, pk):
        course = self.get_object()
        saved_obj, _ = SavedCourse.objects.get_or_create(course=course, user=request.user)
        saved_obj.saved = not saved_obj.saved
        saved_obj.save()
        status = 'Добавлен в сохраненные'
        if not saved_obj.saved:
            status = 'Удалено из сохраненных'
        return Response({'status': status})


class SavedCourseList(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = SavedCourse.objects.all()
    serializer_class = SavedCourseSerializer

    def create(self, request, *args, **kwargs):

        logger.info(f'from saved course - {self.request.user}')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user, saved=True)
        return queryset


class CourseRegisterViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = CourseRegister.objects.all()
    serializer_class = CourseRegisterSerializer

    def create(self, request, *args, **kwargs):

        logger.info(f'from CourseRegister -- {self.request.user}')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseRegisterListSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user,)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchHistoryList(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        if queryset.count() > 3:
            queryset.order_by('-pk').reverse()[0].delete()
        return queryset


