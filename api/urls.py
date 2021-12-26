import rest_framework.authtoken.views
from django.urls import path, include
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, LeaveRoom, UpdateRoom, Registration, UserView


urlpatterns = [
    path('home', RoomView.as_view()),
    path('users', UserView.as_view()),
    path('create_room', CreateRoomView.as_view(), name='create_room'),
    path('get_room', GetRoom.as_view(), name='get_room'),
    path('join_room', JoinRoom.as_view(), name='join_room'),
    path('leave_room', LeaveRoom.as_view(), name='leave_room'),
    path('update_room', UpdateRoom.as_view(), name='update_room'),
    path('auth', include('rest_framework.urls')),
    path('token-auth/', rest_framework.authtoken.views.obtain_auth_token),
    path('token-reg/', Registration.as_view(), name='registration'),
]
