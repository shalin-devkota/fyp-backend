from django.urls import path
from .views import GetUserFromJWT
urlpatterns = [
        path("info/", GetUserFromJWT.as_view(), name="get_user_from_jwt"),

]

