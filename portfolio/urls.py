from django.urls import path
from .views import PortfolioView

urlpatterns = [
    path("me", PortfolioView.as_view(), name="portfolio"),
]

