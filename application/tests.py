from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from application.models import Lesson, Course, CourseSubscription
from users.models import User, UserRoles


class LessonCRUDTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@sky.pro', is_active=True)
        self.user.set_password('1234')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test course')
        self.lesson = Lesson.objects.create(
            name='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )

    def test_lesson_create(self):
        data = {
            'name': 'Test lesson',
            'description': 'Test description',
            'course': self.course.pk,
            'video_link': 'https://www.youtube.com/watch?v=i-uvtDKeFgE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs'
        }
        response = self.client.post(
            reverse('application:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_lesson_list(self):
        response = self.client.get(reverse('application:lesson-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': self.lesson.id,
                'course': self.course.id,  # Serialize course name
                'is_public': False,
                'name': 'Test lesson',
                'description': 'Test description',
                'preview': None,
                'video_link': '',  # Ensure video_link is serialized to None
                'owner': self.lesson.owner.id
            }]
        }

        self.assertEqual(response.json(), expected_data)

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('application:lesson-retrieve',
                    args=[self.lesson.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'is_public': False, 'course': self.course.id, 'name': 'Test lesson',
             'description': 'Test description',
             'preview': None, 'video_link': '', 'owner': self.lesson.owner.id}
        )

    def test_lesson_update(self):
        data = {
            'name': 'Test update name',
            'description': 'Test update description',
            'course': self.course.pk,
            'video_link': 'https://www.youtube.com/watch?v=i-uvtDKeFgE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs'
        }
        response = self.client.put(
            reverse('application:lesson-update', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id,
             'is_public': False,
             'course': self.course.pk,
             'name': 'Test update name',
             'description': 'Test update description',
             'preview': None,
             'video_link': 'https://www.youtube.com/watch?v=i-uvtDKeFgE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs',
             'owner': self.lesson.owner.id}
        )

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse('application:lesson-destroy', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.count(),
            0
        )

    def tearDown(self):
        pass


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@sky.pro', is_active=True, role=UserRoles.MODERATOR)
        self.user.set_password('123')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test course')
        self.lesson = Lesson.objects.create(
            name='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )
        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_subscription_create(self):
        course = Course.objects.create(name='Test course 2')
        course.save()

        data = {
            'course': course.id,
            'user': self.user.id
        }
        response = self.client.post(
            reverse('application:subs-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            CourseSubscription.objects.count(),
            2
        )

    def test_subscription_list(self):
        response = self.client.get(
            reverse('application:subs-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': self.subscription.id, 'is_subscribed': False, 'course': self.subscription.course.id,
              'user': self.subscription.user.id}]
        )

    def test_subscription_delete(self):
        response = self.client.delete(
            reverse('application:subs-delete', args=[self.subscription.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            CourseSubscription.objects.count(),
            0
        )
