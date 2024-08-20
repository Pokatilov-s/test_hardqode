from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer,
                                                  ListAvailableCourseSerializer)  # NEW
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

# NEW start
        user = request.user
        user_balance = get_object_or_404(Balance, user_id=user.id)

        try:
            course = Course.objects.only('id', 'price').get(id=pk)
        except Course.DoesNotExist:
            raise Http404("Курс не найден")

        if user_balance.amount >= course.price:
            if not Subscription.objects.filter(user_id=user.id, course_id=course.id).exists():

                user_balance.amount -= course.price
                user_balance.save()

                serializer = SubscriptionSerializer(
                    data={
                        'user': user.id,
                        'course': course.id
                    }
                )

                serializer.save()

                return Response(
                    data='Подписка на курс приобретена ',
                    status=status.HTTP_201_CREATED
                )

            return Response(
                data='Пользователь уже подписан на курс',
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data='Не достаточно бонусов на балансе',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=ListAvailableCourseSerializer,
        url_path='available'
    )
    def list_courses_available_to_buy(self, request):
        """Получить список доступных для покупки курсов"""
        user_subscriptions = Subscription.objects.filter(
            user=request.user
        ).values_list(
            'course_id',
            flat=True
        )

        courses = Course.objects.only(
            'id',
            'author',
            'title',
            'start_date',
            'price'
        ).filter(
            is_available=True
        ).exclude(
            id__in=user_subscriptions
        ).annotate(
            lesson_count=Count('lessons')
        )
        serializer = ListAvailableCourseSerializer(courses, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

# NEW end
