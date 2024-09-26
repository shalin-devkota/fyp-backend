from django.urls import path
from .views import *
urlpatterns = [
    path("list/", ListStock.as_view(), name="list_all_stock"),
]


