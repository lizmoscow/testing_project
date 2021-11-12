from django.urls import path, include
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, UserInRoom, LeaveRoom, UpdateRoom


urlpatterns = [
    path('home', RoomView.as_view()),
    path('create_room', CreateRoomView.as_view(), name='create_room'),
    path('get_room', GetRoom.as_view(), name='get_room'),
    path('join_room', JoinRoom.as_view(), name='join_room'),
    path('user_in_room', UserInRoom.as_view(), name='user_in_room'),
    path('leave_room', LeaveRoom.as_view(), name='leave_room'),
    path('update_room', UpdateRoom.as_view(), name='update_room'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
