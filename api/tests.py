from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from api.models import Room
from api.serializers import RoomSerializer


class RoomTestCase(TestCase):
    def setUp(self):
        Room.objects.create(host="Alice", guest_can_pause=True, votes_to_skip=6)
        Room.objects.create(host="Bob", guest_can_pause=False, votes_to_skip=4)
        Room.objects.create(host="Charlie", guest_can_pause=False, votes_to_skip=10)
        Room.objects.create(host="Dave", guest_can_pause=True, votes_to_skip=1)

    def test_generate_unique_code(self):
        room = Room.objects.filter(host='Alice')
        self.assertEqual(len(room), 1)
        same_code_rooms = Room.objects.filter(code=room[0].code)
        self.assertEqual(len(same_code_rooms), 1)


class GetRoomTestCase(TestCase):
    def test_get_room_no_code(self):
        response = self.client.get(reverse('get_room'))
        self.assertEqual(response.status_code, 400)

    def test_get_room_wrong_code(self):
        response = self.client.get(reverse('get_room'), {'code': 'ABCDEF'})
        self.assertEqual(response.status_code, 404)

    def test_get_room_existing_code(self):
        Room.objects.create(host="Alice", guest_can_pause=True, votes_to_skip=6)
        room = Room.objects.filter(host='Alice')[0]
        data = RoomSerializer(room).data
        response = self.client.get(reverse('get_room'), {'code': room.code})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['host'])
        self.assertContains(response, data['votes_to_skip'])
        self.assertContains(response, data['code'])
        self.assertContains(response, data['created_at'])


class CreateRoomTestCase(TestCase):

    def test_create_room_incorrect_data(self):
        response = self.client.post(reverse('create_room'), {'votes_to_skip': 'Alice'})
        self.assertEqual(response.status_code, 400)

    def test_create_new_room(self):
        session = self.client.session
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        response = self.client.post(reverse('create_room'), {'votes_to_skip': '4', 'guest_can_pause': 'true'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Room.objects.filter(votes_to_skip='4')), 1)
        room = Room.objects.filter(votes_to_skip='4')[0]
        self.assertEqual(room.host, session.session_key)
        self.assertEqual(room.votes_to_skip, 4)
        self.assertEqual(room.guest_can_pause, True)

    def test_create_existing_room(self):
        session = self.client.session
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        Room.objects.create(host=session.session_key, guest_can_pause=False, votes_to_skip=6)
        response = self.client.post(reverse('create_room'), {'votes_to_skip': '4', 'guest_can_pause': 'True'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Room.objects.filter(votes_to_skip='4')), 1)
        room = Room.objects.filter(votes_to_skip='4')[0]
        self.assertEqual(room.host, session.session_key)
        self.assertEqual(room.votes_to_skip, 4)
        self.assertEqual(room.guest_can_pause, True)


class JoinRoomTestCase(TestCase):

    def test_join_room_incorrect_data_code_none(self):
        response = self.client.post(reverse('join_room'))
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_short_code(self):
        response = self.client.post(reverse('join_room'), {'code': 'ABCD'})
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_long_code(self):
        response = self.client.post(reverse('join_room'), {'code': 'ABCDEFGH'})
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_nonexisting_code(self):
        response = self.client.post(reverse('join_room'), {'code': 'ABCDEF'})
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_lowercase_code(self):
        response = self.client.post(reverse('join_room'), {'code': 'abcdef'})
        self.assertEqual(response.status_code, 400)

    def test_join_room_correct_data_existing_code(self):
        Room.objects.create(code='ABCDEF', host='Alice', guest_can_pause=False, votes_to_skip=6)
        response = self.client.post(reverse('join_room'), {'code': 'ABCDEF'})
        session = self.client.session
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room Joined')
        self.assertEqual(session['room_code'], 'ABCDEF')


class UserInRoomTestCase(TestCase):
    def test_user_in_room(self):
        session = self.client.session
        session['room_code'] = 'ABCDEF'
        session.save()
        response = self.client.get(reverse('user_in_room'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ABCDEF')

    def test_user_not_in_room(self):
        response = self.client.get(reverse('user_in_room'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'null', response.content)


class LeaveRoomTestCase(TestCase):
    def test_user_in_room(self):
        session = self.client.session
        session['room_code'] = 'ABCDEF'
        session.save()
        response = self.client.post(reverse('leave_room'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Success', response.content)

    def test_user_not_in_room(self):
        response = self.client.post(reverse('leave_room'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Success', response.content)


class UpdateRoomTestCase(TestCase):

    def test_update_room_incorrect_data(self):
        response = self.client.patch(reverse('update_room'))
        self.assertEqual(response.status_code, 400)

    def test_update_new_room(self):
        response = self.client.patch(reverse('update_room'), {'votes_to_skip': '4',
                                                              'guest_can_pause': 'true',
                                                              'code': 'ABCDEF'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_someone_elses_room(self):
        Room.objects.create(code='ABCDEF', host='Alice', guest_can_pause=False, votes_to_skip=6)
        response = self.client.patch(reverse('update_room'), {'votes_to_skip': '4',
                                                              'guest_can_pause': 'true',
                                                              'code': 'ABCDEF'}, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_update_existing_room(self):
        session = self.client.session
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        Room.objects.create(code='ABCDEF', host=session.session_key, guest_can_pause=False, votes_to_skip=6)
        response = self.client.patch(reverse('update_room'), {'votes_to_skip': '4',
                                                              'guest_can_pause': 'True',
                                                              'code': 'ABCDEF'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.filter(code='ABCDEF')), 1)
        room = Room.objects.filter(code='ABCDEF')[0]
        self.assertEqual(room.host, session.session_key)
        self.assertEqual(room.votes_to_skip, 4)
        self.assertEqual(room.guest_can_pause, True)
