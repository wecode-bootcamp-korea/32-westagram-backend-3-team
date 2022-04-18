from django.urls import path,include
from . import views
        
urlpatterns = [
    path('/signup',views.UserView.as_view())
]