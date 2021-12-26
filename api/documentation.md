# api
## api/models.py
**def generate_unique_code()** \
`Generates unique Room code` 

### class Room(models.Model)
`Contains information about all virtual music rooms.` \
`Fields:` \
`    * room code (CharField)` \
`    * host (User)` \
`    * guest_can_pause (Boolean)` \
`    * votes_to_skip (Integer)` \
`    * created_at (DateTimeField)` 

> **def get_user_name(self)** \
> `Returns name of the host` 
>

## api/serializers.py
### class RoomSerializer(serializers.ModelSerializer)
`Serializer for Room model` 


### class UserSerializer(serializers.ModelSerializer)
`Serializer for User model` 


### class CreateRoomSerializer(serializers.ModelSerializer)
`Serializes data for CreateRoom view` 


### class UpdateRoomSerializer(serializers.ModelSerializer)
`Serializes data for UpdateRoom view` 


### class RegisterUserSerializer(serializers.ModelSerializer)
`Serializes data for Register view` 



## api/tests.py
### class RoomTestCase(TestCase)
`Test suit for Room model` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_generate_unique_code(self)** \
> `Tests if a room code is unique` 
>
### class RoomTestCaseWithMock(TestCase)
`Test suit for Room model` \
`Uses mocking` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_user_name(self)** \
> `Tests if Room.get_user_name() returns proper username` 
>
### class GetRoomTestCase(TestCase)
`Test suit for GetRoom` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_get_room_not_authenticated(self)** \
> `If user is unauthenticated status code 403 should be returned` 
>
> **def test_get_room_no_code(self)** \
> `If no user code has been passed status code 400 should be returned` 
>
> **def test_get_room_wrong_code(self)** \
> `If a wrong room code has been passed status code 404 should be returned` 
>
> **def test_get_room_existing_code(self)** \
> `If the proper room code has been passed room data should be returned with status code 200` 
>
### class CreateRoomTestCase(TestCase)
`Test suit for :view:`api.CreateRoom`` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_create_room_not_authenticated(self)** \
> `If user is unauthenticated status code 403 should be returned` 
>
> **def test_create_room_incorrect_data(self)** \
> `If incorrect data has been passed status code 400 should be returned` 
>
> **def test_create_new_room(self)** \
> `If a user does not yet has a room a new room created and status code 201 returned` 
>
> **def test_create_existing_room(self)** \
> `If a user already has a room the room is updated  and status code 201 returned` 
>
### class JoinRoomTestCase(TestCase)
`Test suit for :view:`api.JoinRoom`` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_join_room_not_authenticated(self)** \
> `If user is unauthenticated status code 403 should be returned` 
>
> **def test_join_room_incorrect_data(self)** \
> `If no room code has been passed status code 400 should be returned` 
>
> **def test_join_room_incorrect_data_short_code(self)** \
> `If a room code that has been passed is too short status code 400 should be returned` 
>
> **def test_join_room_incorrect_data_long_code(self)** \
> `If a room code that has been passed is too long status code 400 should be returned` 
>
> **def test_join_room_incorrect_data_nonexisting_code(self)** \
> `If a room with the code does not exist status code 400 should be returned` 
>
> **def test_join_room_incorrect_data_lowercase_code(self)** \
> `If a room code that has been passed is lowercase status code 400 should be returned` 
>
> **def test_join_room_correct_data_existing_code(self)** \
> `If an existing room code has been passed room can be joined and status code 200 should be returned` 
>
### class LeaveRoomTestCase(TestCase)
`Test suit for :view:`api.LeaveRoom`` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_leave_room_not_authenticated(self)** \
> `If user is unauthenticated status code 403 should be returned` 
>
> **def test_leave_room_wrong_format(self)** \
> `If no room code has been passed status code 400 should be returned` 
>
> **def test_leave_room_wrong_code(self)** \
> `If a wrong room code has been passed status code 400 should be returned` 
>
> **def test_leave_room_user_is_not_host(self)** \
> `If a user leaving a room is not a host room should not be deleted and status code 200 should be returned` 
>
> **def test_leave_room_user_is_host(self)** \
> `If a user living a room is a host room is deleted and status code 200 should be returned` 
>
### class UpdateRoomTestCase(TestCase)
`Test suit for :view:`api.UpdateRoom`` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_update_room_not_authenticated(self)** \
> `If user is unauthenticated status code 403 should be returned` 
>
> **def test_update_room_incorrect_data(self)** \
> `If no room data has been passed status code 400 should be returned` 
>
> **def test_update_new_room(self)** \
> `If the updated room does not exist status code 404 should be returned` 
>
> **def test_update_someone_elses_room(self)** \
> `If the user is not a host of the updated room status code 403 should be returned` 
>
> **def test_update_existing_room(self)** \
> `If the correct data has been passed the room should be updated and status code 200 should be returned` 
>
### class RegistrationTestCase(TestCase)
`Test suit for :view:`api.Registration`` 

> **def setUp(self)** \
> `Initialises data for the tests` 
>
> **def test_register_incorrect_data(self)** \
> `If no user data has been passed status code 400 should be returned` 
>
> **def test_register_existing_username(self)** \
> `If a user with the name already exists status code 400 should be returned` 
>
> **def test_register_correct_data(self)** \
> `If a new user data has been passed new user should be created and status code 200 should be returned` 
>
> **def test_register_authenticated(self)** \
> `If user is authenticated status code 403 should be returned` 
>

## api/urls.py

## api/views.py
### class RoomView(generics.ListAPIView)
`Returns all Room objects` 

### class UserView(generics.ListAPIView)
`Returns all User objects` 

### class GetRoom(APIView)
`GET method` \
`Receives the code of a Room` \
`Returns the room attributes if the current User is the host` 

> **def get(self, request, format=None)** \
> `None` 
>
### class CreateRoomView(APIView)
`POST method` \
`Receives Room parameters: guest_can_pause, votes_to_skip` \
`Creates a room and returns it` 

> **def post(self, request, format=None)** \
> `None` 
>
### class JoinRoom(APIView)
`POST method` \
`Receives a Room code` \
`Checks if the Room can be joined` 

> **def post(self, request, format=None)** \
> `None` 
>
### class LeaveRoom(APIView)
`POST method` \
`Receives a Room code` \
`If the User is the host deletes the Room` 

> **def post(self, request, format=None)** \
> `None` 
>
### class UpdateRoom(APIView)
`PATCH method` \
`Receives a Room code and new room parameters: guest_can_pause, votes_to_skip` \
`If Room exists and the User is the host updates the room with new parameters` 

> **def patch(self, request, format=None)** \
> `None` 
>
### class Registration(APIView)
`POST method` \
`Receives username and password` \
`If a user with this credentials does not exists and if no user is authenticated, creates a new one` 

> **def post(self, request, format=None)** \
> `None` 
>

