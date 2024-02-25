from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from .models import Course, Lesson, CourseSubscription
from .paginators import CoursePagination, LessonPagination
from .permissions import IsOwner, IsModerator, IsPublic
from .serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from application.tasks import send_course_update, send_lesson_adding

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination  # Добавление класса пагинации

    def get_queryset(self):
        # Если пользователь является модератором, то ему доступны все курсы
        if self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.all().order_by('id')
        else:
            # Возвращаем только те курсы, которые принадлежат текущему пользователю
            return Course.objects.filter(owner=self.request.user).order_by('id')

    def create(self, request, *args, **kwargs):
        """
        Переопределенный метод для создания объекта.
        Проверяет, является ли пользователь модератором перед созданием объекта.
        """
        if request.user.groups.filter(name='moderator').exists():
            raise PermissionDenied("Модераторам запрещено создавать объекты.")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Переопределенный метод для удаления объекта.
        Проверяет, является ли пользователь модератором перед удалением объекта.
        """
        if request.user.groups.filter(name='moderator').exists():
            raise PermissionDenied("Модераторам запрещено удалять объекты.")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Переопределенный метод для сохранения объекта при создании.
        Устанавливает владельца объекта в текущего пользователя.
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course_id = serializer.save(owner=self.request.user).id
        send_course_update.delay(course_id)


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        course_id = serializer.save(owner=self.request.user).course.id
        lesson_id = serializer.save().id
        send_lesson_adding.delay(lesson_id, course_id)



class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator | IsPublic]
    pagination_class = LessonPagination  # Добавление класса пагинации

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all().order_by('id')
        else:
            return Lesson.objects.filter(owner=self.request.user).order_by('id')


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | ~IsModerator]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return CourseSubscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]
