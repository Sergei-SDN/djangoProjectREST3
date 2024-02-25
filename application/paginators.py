from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    page_size = 2  # Количество объектов на одной странице


class LessonPagination(PageNumberPagination):
    page_size = 3  # Количество объектов на одной странице
