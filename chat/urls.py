from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.UsersListView.as_view(), name='threads'),
    path('user/<int:pk>', views.MessagesListView.as_view(), name='messages'),
]