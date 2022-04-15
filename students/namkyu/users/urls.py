from django.urls import path
from users.views import JoinView

urlpatterns = [
    path('/join', JoinView.as_view())
]