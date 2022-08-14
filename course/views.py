import logging

from django.db.models import Q, Count, Case, When, ExpressionWrapper
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from course.models import *
from course.permission import IsTeacherUser
from course.serializers import *

logger = logging.getLogger('')


class ReviewViewSet(ModelViewSet):
    """
    crud for the model Review, when get request user will get only his review, and here logger with warning level
    """
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all().select_related('user')
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

# .annotate(student_count=Count('courseregister', distinct=True), сom=Count(Case(When(review__description=True, then=1,))),
#                                              likes=Count(Case(When(like__like=True, then=1), distinct=True))).prefetch_related('lessons').select_related('adviser')

# (com=Count('review__description', filter=Q(review__description__isnull=False)),
#                                              allocated=Count('pk', filter=Q(review__description__isnull=None))
#                                              )

class CourseViewSet(ModelViewSet):
    """
    crud for the model Course, with annotate to get likes and with prefetch_related, select_related
    to optimize sql requests, when user get all course there will be number of descriptions but when user
    get course by ID there will be all descriptions, and here logger with warning level
    """
    queryset = Course.objects.all().annotate(student_count=Count('courseregister', distinct=True)
                                             ).prefetch_related('lessons').select_related('adviser')

    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'saved', 'like']:
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'put', 'partial_update']:
            permissions = [IsTeacherUser]
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

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        if self.get_object().adviser != request.user:
            raise ValueError('You are not teacher of this course')
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

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
        status = 'Added to saved'
        if not saved_obj.saved:
            status = 'Removed from saved'
        return Response({'status': status})


class SavedCourseList(ListAPIView):
    """
    ListApiView the model SavedCourse, user must be authenticated, here used select_related
    to optimize sql request, and here logger with warning level, to save some course user use CourseViewSet
    """
    permission_classes = [IsAuthenticated]

    queryset = SavedCourse.objects.all().select_related('course', 'user')
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
    """
    viewset for crud for the model CourseRegister, here used select_related to optimize sql requests,
    also here user logger with warning level
    """
    permission_classes = [IsAuthenticated]

    queryset = CourseRegister.objects.all().select_related('course', 'user')
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
    """
    ListApiView for SearchHistory, will show only last 3 search course,
    """
    permission_classes = [IsAuthenticated]
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        if queryset.count() > 3:
            queryset.order_by('-pk').reverse()[0].delete()
        return queryset


