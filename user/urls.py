from django.urls import path
from .views import GetUserFromJWT, UserTransactions,LoadFunds,GetFunds
urlpatterns = [
        path("info/", GetUserFromJWT.as_view(), name="get_user_from_jwt"),
        path("transactions/", UserTransactions.as_view(), name="user_transactions"),
        path("load-funds/", LoadFunds.as_view(), name="load_funds"),
        path("get-funds/", GetFunds.as_view(), name="get_funds"),	
]

