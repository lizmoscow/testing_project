from django.urls import path
from .views import RoomView, CreateRoomView


urlpatterns = [
    path('home', RoomView.as_view()),
    path('create_room', CreateRoomView.as_view()),
]
