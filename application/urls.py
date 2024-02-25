from django.urls import path, include
from rest_framework.routers import DefaultRouter
from application.apps import ApplicationConfig
from application.views import CourseViewSet, LessonListView, \
    LessonUpdateView, LessonDestroyView, LessonCreateView, LessonRetrieveView, SubscriptionListAPIView, \
    SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = ApplicationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('api/lessons/list', LessonListView.as_view(), name='lesson-list'),
    path('api/lessons/retrieve/<int:pk>/', LessonRetrieveView.as_view(),
         name='lesson-retrieve'),
    path('api/lessons/update/<int:pk>/', LessonUpdateView.as_view(),
         name='lesson-update'),
    path('api/lessons/destroy/<int:pk>/', LessonDestroyView.as_view(),
         name='lesson-destroy'),

    # subscription
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subs-list'),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subs-create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subs-delete'),

]  # + router.urls
