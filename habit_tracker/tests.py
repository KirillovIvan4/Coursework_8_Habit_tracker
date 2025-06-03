from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit_tracker.models import Days, Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым теcтом
        self.user = User.objects.create(email='admin@admin.com')
        self.days = Days.objects.create(days='mon')
        self.habit = Habit.objects.create(place='Test_place',
                                          time='12:00:00',
                                          action='Test_action',
                                          time_to_perform='00:02:00',
                                          publicity_indicator=True,
                                          pleasant_habit_indicator=True,
                                          creator=self.user)
        self.client.force_authenticate(user=self.user)
        self.habit.frequency.set([self.days])

    def test_habit_retrieve(self):
        url = reverse('habit_tracker:habit-get',
                      args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('place'), self.habit.place
        )

    def test_habit_create(self):
        url = reverse('habit_tracker:habit-create')
        data = {
            'place': 'Test_place',
            'time': '12:00:00',
            'action': 'Test_action',
            'time_to_perform': '00:02:00',
            'frequency': [self.days.pk],
            'publicity_indicator': True,
            'pleasant_habit_indicator': True,
        }
        response = self.client.post(url, data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Habit.objects.all().count(), 2
        )

    def test_habit_update(self):
        url = reverse('habit_tracker:habit-update', args=(self.habit.pk,))
        data = {'place':'Test_place_2'}
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get('place'), 'Test_place_2'
        )

    def test_habit_delete(self):
        url = reverse('habit_tracker:habit-delete', args=(self.habit.pk,))
        response = self.client.delete(url)
        print(response.data)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Habit.objects.all().count(), 0
        )

    def test_habit_list(self):
        url = reverse('habit_tracker:habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 1)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 1)

        habit_data = response.data['results'][0]
        self.assertEqual(habit_data['id'], self.habit.pk)
        self.assertEqual(habit_data['place'], self.habit.place)
        self.assertEqual(habit_data['creator'], self.habit.creator.pk)

        if 'url' in habit_data:
            self.assertIsNone(habit_data['url'])
