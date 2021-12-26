from rest_framework import generics, status
from .serializers import RoomSerializer, \
                         CreateRoomSerializer, \
                         UpdateRoomSerializer, \
                         RegisterUserSerializer, UserSerializer
from .models import Room
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response


class RoomView(generics.ListAPIView):
    """
    Returns all Room objects
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserView(generics.ListAPIView):
    """
    Returns all User objects
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetRoom(APIView):
    """
    GET method
    Receives the code of a Room
    Returns the room attributes if the current User is the host
    """
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = request.user == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code Parameter Not Found in Request'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    """
    POST method
    Receives Room parameters: guest_can_pause, votes_to_skip
    Creates a room and returns it
    """
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = request.user
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.votes_to_skip = votes_to_skip
                room.guest_can_pause = guest_can_pause
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    """
    POST method
    Receives a Room code
    Checks if the Room can be joined
    """
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                return Response({'Message': "Room Joined"}, status=status.HTTP_200_OK)
            return Response({'Bad Request': "Invalid room code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': "Invalid post data, did not find a code key"}, status=status.HTTP_400_BAD_REQUEST)


class LeaveRoom(APIView):
    """
    POST method
    Receives a Room code
    If the User is the host deletes the Room
    """
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_results = Room.objects.filter(code=code)
            if len(room_results) > 0:
                room = room_results[0]
                if room.host == request.user:
                    room.delete()
                return Response({'Message': 'Success'}, status=status.HTTP_200_OK)
            return Response({'Bad Request': "Invalid room code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': "Invalid post data, did not find a code key"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateRoom(APIView):
    """
    PATCH method
    Receives a Room code and new room parameters: guest_can_pause, votes_to_skip
    If Room exists and the User is the host updates the room with new parameters
    """
    serializerClass = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializerClass(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')
            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'Message': "Room not found"}, status=status.HTTP_404_NOT_FOUND)
            room = queryset[0]
            user_id = request.user
            if room.host != user_id:
                return Response({'Message': "You are not the host"}, status=status.HTTP_403_FORBIDDEN)
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)


class Registration(APIView):
    """
    POST method
    Receives username and password
    If a user with this credentials does not exists and if no user is authenticated, creates a new one
    """
    serializerClass = RegisterUserSerializer

    def post(self, request, format=None):
        if request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializerClass(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            queryset = User.objects.filter(username=username)
            User.objects.create_user(username=username, password=password)
            user = User.objects.filter(username=username)
            token = Token.objects.create(user=user[0])
            return Response({'token': token.key, 'username': username}, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
