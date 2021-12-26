from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Room, generate_unique_code
from rest_framework.test import force_authenticate, APIRequestFactory
from .views import CreateRoomView, GetRoom, JoinRoom, LeaveRoom, UpdateRoom, Registration
from api.serializers import RoomSerializer


class RoomTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        Room.objects.create(host=User.objects.filter(username="Alice")[0], guest_can_pause=True, votes_to_skip=6)
        User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)
        User.objects.create_user(username="Charlie", email="c@c.c", password="ccccccc")
        Room.objects.create(host=User.objects.filter(username="Charlie")[0], guest_can_pause=False, votes_to_skip=10)
        User.objects.create_user(username="Dave", email="d@d.d", password="ddddddd")
        Room.objects.create(host=User.objects.filter(username="Dave")[0], guest_can_pause=True, votes_to_skip=1)

    def test_generate_unique_code(self):
        room = Room.objects.filter(host=User.objects.filter(username="Alice")[0])
        self.assertEqual(len(room), 1)
        same_code_rooms = Room.objects.filter(code=room[0].code)
        self.assertEqual(len(same_code_rooms), 1)


class GetRoomTestCase(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        self.user = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.room = Room.objects.create(host=self.user, guest_can_pause=True, votes_to_skip=6)

    def test_get_room_not_authenticated(self):
        request = self.factory.get('/get_room')
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_get_room_no_code(self):
        request = self.factory.get('/get_room')
        force_authenticate(request, user=self.user)
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_get_room_wrong_code(self):
        request = self.factory.get('/get_room?code=ABCDEF')
        force_authenticate(request, user=self.user)
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_get_room_existing_code(self):
        data = RoomSerializer(self.room).data
        request = self.factory.get(f'/get_room?code={self.room.code}')
        force_authenticate(request, user=self.user)
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['host'])
        self.assertContains(response, data['votes_to_skip'])
        self.assertContains(response, data['code'])
        self.assertContains(response, data['created_at'])


class CreateRoomTestCase(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        self.user = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")

    def test_create_room_not_authenticated(self):
        request = self.factory.post('/create_room', {'votes_to_skip': 'Alice'})
        response = CreateRoomView.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_room_incorrect_data(self):
        request = self.factory.post('/create_room', {'votes_to_skip': 'Alice'})
        force_authenticate(request, user=self.user)
        response = CreateRoomView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_create_new_room(self):
        request = self.factory.post('/create_room', {'votes_to_skip': '4', 'guest_can_pause': 'True'})
        force_authenticate(request, user=self.user)
        response = CreateRoomView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Room.objects.filter(votes_to_skip='4')), 1)
        room = Room.objects.filter(votes_to_skip='4')[0]
        self.assertEqual(room.host, self.user)
        self.assertEqual(room.votes_to_skip, 4)
        self.assertEqual(room.guest_can_pause, True)

    def test_create_existing_room(self):
        self.room = Room.objects.create(host=self.user, guest_can_pause=False, votes_to_skip=6)
        request = self.factory.post('/create_room', {'votes_to_skip': '4', 'guest_can_pause': 'True'})
        force_authenticate(request, user=self.user)
        response = CreateRoomView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Room.objects.filter(votes_to_skip='4')), 1)
        room = Room.objects.filter(votes_to_skip='4')[0]
        self.assertEqual(room.host, self.user)
        self.assertEqual(room.votes_to_skip, 4)
        self.assertEqual(room.guest_can_pause, True)


class JoinRoomTestCase(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.userB = User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        self.room = Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)

    def test_join_room_not_authenticated(self):
        request = self.factory.post('/join_room', {'code': self.room.code})
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_join_room_incorrect_data_code_none(self):
        request = self.factory.post('/join_room')
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_short_code(self):
        request = self.factory.post('/join_room', {'code': 'ABCD'})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_long_code(self):
        request = self.factory.post('/join_room', {'code': 'ABCDEFGH'})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_nonexisting_code(self):
        request = self.factory.post('/join_room', {'code': generate_unique_code()})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_lowercase_code(self):
        request = self.factory.post('/join_room', {'code': 'abcdef'})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_correct_data_existing_code(self):
        request = self.factory.post('/join_room', {'code': self.room.code})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room Joined')


class LeaveRoomTestCase(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.userB = User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        self.room = Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)

    def test_leave_room_not_authenticated(self):
        request = self.factory.post('/leave_room', {'code': self.room.code})
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_leave_room_wrong_format(self):
        request = self.factory.post('/leave_room')
        force_authenticate(request, user=self.userA)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_leave_room_wrong_code(self):
        request = self.factory.post('/leave_room', {'code': generate_unique_code()})
        force_authenticate(request, user=self.userA)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_leave_room_user_is_not_host(self):
        code = self.room.code
        request = self.factory.post('/leave_room', {'code': code})
        force_authenticate(request, user=self.userA)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.filter(code=code)), 1)

    def test_leave_room_user_is_host(self):
        code = self.room.code
        request = self.factory.post('/leave_room', {'code': code})
        force_authenticate(request, user=self.userB)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.filter(code=code)), 0)


class UpdateRoomTestCase(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.userB = User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        self.room = Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)

    def test_update_room_not_authenticated(self):
        request = self.factory.patch('/update_room', {'code': self.room.code,
                                                     'votes_to_skip': '4',
                                                     'guest_can_pause': 'True'})
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_update_room_incorrect_data(self):
        request = self.factory.patch('/update_room')
        force_authenticate(request, user=self.userA)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_update_new_room(self):
        request = self.factory.patch('/update_room', {'votes_to_skip': '4',
                                                      'guest_can_pause': 'true',
                                                      'code': generate_unique_code()})
        force_authenticate(request, user=self.userA)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_update_someone_elses_room(self):
        request = self.factory.patch('/update_room', {'votes_to_skip': '4',
                                                      'guest_can_pause': 'true',
                                                      'code': self.room.code})
        force_authenticate(request, user=self.userA)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_update_existing_room(self):
        request = self.factory.patch('/update_room', {'votes_to_skip': '4',
                                                      'guest_can_pause': 'true',
                                                      'code': self.room.code})
        force_authenticate(request, user=self.userB)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.filter(code=self.room.code)), 1)
        room = Room.objects.filter(code=self.room.code)[0]
        self.assertEqual(room.host, self.userB)
        self.assertEqual(room.votes_to_skip, 4)
        self.assertEqual(room.guest_can_pause, True)
