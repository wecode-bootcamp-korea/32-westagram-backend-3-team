from django.urls import path,include
from . import views
        
urlpatterns = [path('/signup',views.Userview.as_view())
]