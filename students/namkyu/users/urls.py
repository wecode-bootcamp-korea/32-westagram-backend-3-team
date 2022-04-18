from django.urls import path
from users.views import RegisterView

urlpatterns = [
    path('/join', RegisterView.as_view())
]