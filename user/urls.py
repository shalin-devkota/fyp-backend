from django.urls import path
from .views import GetUserFromJWT, UserTransactions
urlpatterns = [
        path("info/", GetUserFromJWT.as_view(), name="get_user_from_jwt"),
        path("transactions/", UserTransactions.as_view(), name="user_transactions"),
]

