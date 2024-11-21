from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User
from rest_framework import status
from django.urls import reverse


class LessonTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create(email="owner@sky.pro")
        self.course = Course.objects.create(name="дизайнер", owner=self.owner)
        self.lesson1 = Lesson.objects.create(
            name="Основы дизайна", course=self.course, owner=self.owner
        )
        self.lesson2 = Lesson.objects.create(
            name="Продвинутый дизайн", course=self.course
        )
        self.client.force_authenticate(user=self.owner)

    def test_lesson_retrieve(self):
        url_lesson1 = reverse("materials:lesson-retrieve", args=(self.lesson1.pk,))
        response_lesson1 = self.client.get(url_lesson1)
        data_lesson1 = response_lesson1.json()
        url_lesson2 = reverse("materials:lesson-retrieve", args=(self.lesson2.pk,))
        response_lesson2 = self.client.get(url_lesson2)
        data_lesson2 = response_lesson2.json()

        self.assertEqual(response_lesson1.status_code, status.HTTP_200_OK)
        self.assertEqual(data_lesson1.get("name"), self.lesson1.name)
        # Проверка на permissions контроллера
        self.assertEqual(
            data_lesson2.get("detail"),
            "You do not have permission to perform this action.",
        )
        self.assertEqual(response_lesson2.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        pre_data = {"name": "Дизайн для профи"}
        response = self.client.post(url, data=pre_data)
        data = response.json()
        self.assertEqual(Lesson.objects.all().count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("owner"), self.owner.pk)

    def test_lesson_update(self):
        url_lesson1 = reverse("materials:lesson_update", args=(self.lesson1.pk,))
        url_lesson2 = reverse("materials:lesson_update", args=(self.lesson2.pk,))
        pre_data = {"name": "Основы дизайна 2"}
        response_lesson1 = self.client.patch(url_lesson1, data=pre_data)
        response_lesson2 = self.client.patch(url_lesson2, data=pre_data)
        data_lesson1 = response_lesson1.json()
        data_lesson2 = response_lesson2.json()
        self.assertEqual(data_lesson1.get("name"), "Основы дизайна 2")
        self.assertEqual(response_lesson1.status_code, status.HTTP_200_OK)
        # Проверка на permissions контроллера
        self.assertEqual(
            data_lesson2.get("detail"),
            "You do not have permission to perform this action.",
        )
        self.assertEqual(response_lesson2.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        results = [
            {
                "id": self.lesson1.pk,
                "name": self.lesson1.name,
                "description": self.lesson1.description,
                "preview": self.lesson1.preview,
                "link": self.lesson1.link,
                "course": self.lesson1.course.id,
                "owner": self.lesson1.owner.id,
            },
            {
                "id": self.lesson2.pk,
                "name": self.lesson2.name,
                "description": self.lesson2.description,
                "preview": self.lesson2.preview,
                "link": self.lesson2.link,
                "course": self.lesson2.course.id,
                "owner": self.lesson2.owner,
            },
        ]
        self.assertEqual(data.get("results"), results)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_destroy(self):
        url_lesson1 = reverse("materials:lesson_delete", args=(self.lesson1.pk,))
        response_lesson1 = self.client.delete(url_lesson1)
        url_lesson2 = reverse("materials:lesson_delete", args=(self.lesson2.pk,))
        response_lesson2 = self.client.delete(url_lesson2)
        data_lesson2 = response_lesson2.json()
        self.assertEqual(response_lesson1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(response_lesson2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            data_lesson2.get("detail"),
            "You do not have permission to perform this action.",
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="дизайнер", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Основы дизайна", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        self.sub = Subscription.objects.create(owner=self.user, course=self.course)

    def test_toggle_subscription(self):
        url = reverse("materials:toggle_subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "Подписка удалена")
        response = self.client.post(url, data=data)
        self.assertEqual(response.json().get("message"), "Подписка добавлена")


class CoursesTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create(email="owner@sky.pro")
        self.course1 = Course.objects.create(name="дизайнер", owner=self.owner)
        self.course2 = Course.objects.create(name="инженер")
        # self.lesson1 = Lesson.objects.create(
        #     name="Основы дизайна", course=self.course, owner=self.owner
        # )
        # self.lesson2 = Lesson.objects.create(
        #     name="Продвинутый дизайн", course=self.course
        # )
        self.client.force_authenticate(user=self.owner)

    def test_course_retrieve(self):
        url_course1 = reverse("materials:courses-detail", args=(self.course1.pk,))
        response_course1 = self.client.get(url_course1)
        data = response_course1.json()
        url_course2 = reverse("materials:courses-detail", args=(self.course2.pk,))
        response_course2 = self.client.get(url_course2)

        self.assertEqual(response_course1.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course1.name)
        # Проверка retrieve курса, если пользователь не владелец
        self.assertEqual(response_course2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_course2.json().get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_course_create(self):
        url = reverse("materials:courses-list")
        pre_data = {"name": "backend-developer"}
        response = self.client.post(url, data=pre_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("owner"), self.owner.pk)
        self.assertEqual(data.get("name"), pre_data.get("name"))

    def test_course_update(self):
        pre_data = {"name": "backend_developer2"}
        url_course1 = reverse("materials:courses-detail", args=(self.course1.pk,))
        response_course1 = self.client.patch(url_course1, pre_data)
        data_course1 = response_course1.json()

        url_course2 = reverse("materials:courses-detail", args=(self.course2.pk,))
        response_course2 = self.client.patch(url_course2, pre_data)
        data_course2 = response_course2.json()

        self.assertEqual(response_course1.status_code, status.HTTP_200_OK)
        self.assertEqual(data_course1.get("name"), pre_data.get("name"))
        # Проверка permissions
        self.assertEqual(response_course2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            data_course2.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_course_destroy(self):
        url_course1 = reverse("materials:courses-detail", args=(self.course1.pk,))
        response_course1 = self.client.delete(url_course1)

        url_course2 = reverse("materials:courses-detail", args=(self.course2.pk,))
        response_course2 = self.client.delete(url_course2)

        self.assertEqual(response_course1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 1)
        # Проверка permissions
        self.assertEqual(response_course2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_course2.json().get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_course_list(self):
        url = reverse("materials:courses-list")
        response = self.client.get(url)
        data = response.json().get("results")
        results = [
            {
                "id": self.course1.pk,
                "name": self.course1.name,
                "description": self.course1.description,
                "lessons_count": Lesson.objects.filter(course=self.course1).count(),
                "lessons": list(Lesson.objects.filter(course=self.course1)),
                "owner": self.course1.owner.pk,
                "is_sub": False,
            },
            {
                "id": self.course2.pk,
                "name": self.course2.name,
                "description": self.course2.description,
                "lessons_count": Lesson.objects.filter(course=self.course2).count(),
                "lessons": list(Lesson.objects.filter(course=self.course2)),
                "owner": self.course2.owner,
                "is_sub": False,
            },
        ]
        self.assertEqual(
            data,
            results
        )

