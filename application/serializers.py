from rest_framework import serializers
from .models import Course, Lesson, CourseSubscription
from .validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson."""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video_link'),
                      serializers.UniqueTogetherValidator(fields=['video_link', 'name'], queryset=Lesson.objects.all())]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course."""
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    # Добавляем поле подписки пользователя на курс
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons(self, obj):
        """Метод для получения списка уроков курса."""  # Вычисляемые значения
        lessons = Lesson.objects.filter(course=obj)
        lesson_serializer = LessonSerializer(lessons, many=True)
        return lesson_serializer.data

    def get_lessons_count(self, obj):
        """Метод для получения количества уроков курса."""  # Вычисляемые значения
        return obj.lessons.count()

    def get_is_subscribed(self, instance):
        return CourseSubscription.objects.filter(course=instance,
                                                 user=self.context['request'].user).exists()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(fields=['name'],
                                                queryset=Course.objects.all())
        ]


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(fields=['course'],
                                                queryset=CourseSubscription.objects.all())]
