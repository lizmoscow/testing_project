from django.http import JsonResponse
from django.shortcuts import render
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
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetRoom(APIView):
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
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        # if not self.request.session.exists(self.request.session.session_key):
        #    self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            # host = self.request.session.session_key
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
            # self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        # if not self.request.session.exists(self.request.session.session_key):
        #    self.request.session.create()
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                # self.request.session['room_code'] = code
                return Response({'Message': "Room Joined"}, status=status.HTTP_200_OK)
            return Response({'Bad Request': "Invalid room code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': "Invalid post data, did not find a code key"}, status=status.HTTP_400_BAD_REQUEST)


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'Bad Request': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        host_id = request.user
        room_results = Room.objects.filter(host=host_id)
        if len(room_results) > 0:
            room = room_results[0]
            room.delete()
        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)


class UpdateRoom(APIView):
    serializerClass = UpdateRoomSerializer

    def patch(self, request, format=None):
        # if not self.request.session.exists(self.request.session.session_key):
        #    self.request.session.create()
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
    serializerClass = RegisterUserSerializer

    def post(self, request, format=None):
        serializer = self.serializerClass(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            queryset = User.objects.filter(username=username)
            if queryset.exists():
                return Response({'Message': "User with this name already exists"}, status=status.HTTP_409_CONFLICT)
            User.objects.create_user(username=username, password=password)
            user = User.objects.filter(username=username)
            token = Token.objects.create(user=user[0])
            return Response({'token': token.key, 'username': username}, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
