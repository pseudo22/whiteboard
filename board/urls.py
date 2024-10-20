from django.urls import path
from .views import *

urlpatterns = [
    path('', RoomCreationView.as_view(), name='room_create'),

    path('room/<str:room_name>/', BoardWithChatView.as_view(), name='board_with_chat'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register , name='register')
]
