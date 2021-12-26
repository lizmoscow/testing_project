from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory
import mock
from api.models import Room, generate_unique_code
from .views import CreateRoomView, GetRoom, JoinRoom, LeaveRoom, UpdateRoom, Registration
from api.serializers import RoomSerializer


class RoomTestCase(TestCase):
    """
    Test suit for Room model
    """
    def setUp(self):
        """
        Initialises data for the tests
        """
        User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        Room.objects.create(host=User.objects.filter(username="Alice")[0], guest_can_pause=True, votes_to_skip=6)
        User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbb")
        Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=8)
        User.objects.create_user(username="Cody", email="c@c.c", password="cccccccc")
        Room.objects.create(host=User.objects.filter(username="Cody")[0], guest_can_pause=True, votes_to_skip=10)
        User.objects.create_user(username="Denise", email="d@d.d", password="dddddddd")
        Room.objects.create(host=User.objects.filter(username="Denise")[0], guest_can_pause=False, votes_to_skip=12)

    def test_generate_unique_code(self):
        """
        Tests if a room code is unique
        """
        room = Room.objects.filter(host=User.objects.filter(username="Alice")[0])
        self.assertEqual(len(room), 1)
        same_code_rooms = Room.objects.filter(code=room[0].code)
        self.assertEqual(len(same_code_rooms), 1)


class RoomTestCaseWithMock(TestCase):
    """
    Test suit for Room model
    Uses mocking
    """
    def setUp(self):
        """
        Initialises data for the tests
        """
        self.user = mock.Mock(spec=User)
        self.user._state = mock.Mock()
        self.user.username = "Alice"
        self.room = Room()
        self.room.host = self.user

    def test_user_name(self):
        """
        Tests if Room.get_user_name() returns proper username
        """
        self.assertEqual(self.room.get_user_name(), "Alice")


class GetRoomTestCase(TestCase):
    """
    Test suit for GetRoom
    """
    factory = APIRequestFactory()

    def setUp(self):
        """
        Initialises data for the tests
        """
        self.user = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.room = Room.objects.create(host=self.user, guest_can_pause=True, votes_to_skip=6)

    def test_get_room_not_authenticated(self):
        """
        If user is unauthenticated status code 403 should be returned
        """
        request = self.factory.get('/get_room')
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_get_room_no_code(self):
        """
        If no user code has been passed status code 400 should be returned
        """
        request = self.factory.get('/get_room')
        force_authenticate(request, user=self.user)
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_get_room_wrong_code(self):
        """
        If a wrong room code has been passed status code 404 should be returned
        """
        request = self.factory.get('/get_room?code=ABCDEF')
        force_authenticate(request, user=self.user)
        response = GetRoom.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_get_room_existing_code(self):
        """
        If the proper room code has been passed room data should be returned with status code 200
        """
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
    """
    Test suit for :view:`api.CreateRoom`
    """
    factory = APIRequestFactory()

    def setUp(self):
        """
        Initialises data for the tests
        """
        self.user = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")

    def test_create_room_not_authenticated(self):
        """
        If user is unauthenticated status code 403 should be returned
        """
        request = self.factory.post('/create_room', {'votes_to_skip': 'Alice'})
        response = CreateRoomView.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_room_incorrect_data(self):
        """
        If incorrect data has been passed status code 400 should be returned
        """
        request = self.factory.post('/create_room', {'votes_to_skip': 'Alice'})
        force_authenticate(request, user=self.user)
        response = CreateRoomView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_create_new_room(self):
        """
        If a user does not yet has a room a new room created and status code 201 returned
        """
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
        """
        If a user already has a room the room is updated  and status code 201 returned
        """
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
    """
    Test suit for :view:`api.JoinRoom`
    """
    factory = APIRequestFactory()

    def setUp(self):
        """
        Initialises data for the tests
        """
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.userB = User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        self.room = Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)

    def test_join_room_not_authenticated(self):
        """
        If user is unauthenticated status code 403 should be returned
        """
        request = self.factory.post('/join_room', {'code': self.room.code})
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_join_room_incorrect_data(self):
        """
        If no room code has been passed status code 400 should be returned
        """
        request = self.factory.post('/join_room')
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_short_code(self):
        """
        If a room code that has been passed is too short status code 400 should be returned
        """
        request = self.factory.post('/join_room', {'code': 'ABCD'})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_long_code(self):
        """
        If a room code that has been passed is too long status code 400 should be returned
        """
        request = self.factory.post('/join_room', {'code': 'ABCDEFGH'})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_nonexisting_code(self):
        """
        If a room with the code does not exist status code 400 should be returned
        """
        request = self.factory.post('/join_room', {'code': generate_unique_code()})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_incorrect_data_lowercase_code(self):
        """
        If a room code that has been passed is lowercase status code 400 should be returned
        """
        request = self.factory.post('/join_room', {'code': 'abcdef'})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_join_room_correct_data_existing_code(self):
        """
        If an existing room code has been passed room can be joined and status code 200 should be returned
        """
        request = self.factory.post('/join_room', {'code': self.room.code})
        force_authenticate(request, user=self.userA)
        response = JoinRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room Joined')


class LeaveRoomTestCase(TestCase):
    """
    Test suit for :view:`api.LeaveRoom`
    """
    factory = APIRequestFactory()

    def setUp(self):
        """
        Initialises data for the tests
        """
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.userB = User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        self.room = Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)

    def test_leave_room_not_authenticated(self):
        """
        If user is unauthenticated status code 403 should be returned
        """
        request = self.factory.post('/leave_room', {'code': self.room.code})
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_leave_room_wrong_format(self):
        """
        If no room code has been passed status code 400 should be returned
        """
        request = self.factory.post('/leave_room')
        force_authenticate(request, user=self.userA)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_leave_room_wrong_code(self):
        """
        If a wrong room code has been passed status code 400 should be returned
        """
        request = self.factory.post('/leave_room', {'code': generate_unique_code()})
        force_authenticate(request, user=self.userA)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_leave_room_user_is_not_host(self):
        """
        If a user leaving a room is not a host room should not be deleted and status code 200 should be returned
        """
        code = self.room.code
        request = self.factory.post('/leave_room', {'code': code})
        force_authenticate(request, user=self.userA)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.filter(code=code)), 1)

    def test_leave_room_user_is_host(self):
        """
        If a user living a room is a host room is deleted and status code 200 should be returned
        """
        code = self.room.code
        request = self.factory.post('/leave_room', {'code': code})
        force_authenticate(request, user=self.userB)
        response = LeaveRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.filter(code=code)), 0)


class UpdateRoomTestCase(TestCase):
    """
    Test suit for :view:`api.UpdateRoom`
    """
    factory = APIRequestFactory()

    def setUp(self):
        """
        Initialises data for the tests
        """
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")
        self.userB = User.objects.create_user(username="Bob", email="b@b.b", password="bbbbbbbb")
        self.room = Room.objects.create(host=User.objects.filter(username="Bob")[0], guest_can_pause=False, votes_to_skip=4)

    def test_update_room_not_authenticated(self):
        """
        If user is unauthenticated status code 403 should be returned
        """
        request = self.factory.patch('/update_room', {'code': self.room.code,
                                                     'votes_to_skip': '4',
                                                     'guest_can_pause': 'True'})
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_update_room_incorrect_data(self):
        """
        If no room data has been passed status code 400 should be returned
        """
        request = self.factory.patch('/update_room')
        force_authenticate(request, user=self.userA)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_update_new_room(self):
        """
        If the updated room does not exist status code 404 should be returned
        """
        request = self.factory.patch('/update_room', {'votes_to_skip': '4',
                                                      'guest_can_pause': 'true',
                                                      'code': generate_unique_code()})
        force_authenticate(request, user=self.userA)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_update_someone_elses_room(self):
        """
        If the user is not a host of the updated room status code 403 should be returned
        """
        request = self.factory.patch('/update_room', {'votes_to_skip': '4',
                                                      'guest_can_pause': 'true',
                                                      'code': self.room.code})
        force_authenticate(request, user=self.userA)
        response = UpdateRoom.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_update_existing_room(self):
        """
        If the correct data has been passed the room should be updated and status code 200 should be returned
        """
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


class RegistrationTestCase(TestCase):
    """
    Test suit for :view:`api.Registration`
    """
    factory = APIRequestFactory()

    def setUp(self):
        """
        Initialises data for the tests
        """
        self.userA = User.objects.create_user(username="Alice", email="a@a.a", password="aaaaaaaa")

    def test_register_incorrect_data(self):
        """
        If no user data has been passed status code 400 should be returned
        """
        request = self.factory.post('/token-reg')
        response = Registration.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_register_existing_username(self):
        """
        If a user with the name already exists status code 400 should be returned
        """
        request = self.factory.post('/token-reg', {'username': 'Alice', 'password': 'bbbbbbb'})
        response = Registration.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_register_correct_data(self):
        """
        If a new user data has been passed new user should be created and status code 200 should be returned
        """
        request = self.factory.post('/token-reg', {'username': 'Bob', 'password': 'bbbbbbb'})
        response = Registration.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bob")
        self.assertEqual(len(User.objects.filter(username='Bob')), 1)

    def test_register_authenticated(self):
        """
        If user is authenticated status code 403 should be returned
        """
        request = self.factory.post('/token-reg', {'username': 'Bob', 'password': 'bbbbbbb'})
        force_authenticate(request, user=self.userA)
        response = Registration.as_view()(request)
        self.assertEqual(response.status_code, 403)
