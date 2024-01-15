from rest_framework.test import APITransactionTestCase
from rest_framework import status
from habits.models import Habit
from users.models import User


class CursesAPITestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        self.url = '/habits/'
        User.objects.create(
            email='test1@tes.tes',
            password='12345',
            is_active=True)
        self.user = User.objects.get(email='test1@tes.tes')
        self.data = Habit.objects.create(
            place="Test_place", action='Test_action',
            period=5, is_public=True, owner=self.user,
            time_do_it='2024-01-15T13:26:26.322627+03:00')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            "place": "Test_place_create",
            "action": "Test_action",
            "period": 4,
            "is_public": False,
            "prize": "cake",
            'time_to_complete': 50,
        }
        response = self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_public(self):
        response = self.client.get(self.url + 'public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json(), {'count': 1,
                                           'next': None,
                                           'previous': None,
                                           'results': [
                                               {'action': 'Test_action',
                                                'place': 'Test_place',
                                                'time_do_it': '2024-01-15T'
                                                              '13:26:26.322627'
                                                              '+03:00',
                                                'related_habit': None,
                                                'prize': None,
                                                'time_to_complete': 30}]}
                         )

    def test_list(self):
        response = self.client.get(
            self.url,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json(), {'count': 1,
                                           'next': None,
                                           'previous': None,
                                           'results': [
                                               {'action': 'Test_action',
                                                'place': 'Test_place',
                                                'time_do_it': '2024-01-15T13'
                                                              ':26:26.322627'
                                                              '+03:00',
                                                'related_habit': None,
                                                'prize': None,
                                                'time_to_complete': 30}]}
                         )

    def test_retrieve(self):
        responce = self.client.get(
            self.url + '1/'
        )
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.json(), {'action': 'Test_action',
                                           'place': 'Test_place',
                                           'time_do_it': '2024-01-15T13:26'
                                                         ':26.322627+03:00',
                                           'related_habit': None,
                                           'prize': None,
                                           'time_to_complete': 30}
                         )

    def test_destroy(self):
        responce = self.client.delete(
            self.url + '1/'
        )

        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
