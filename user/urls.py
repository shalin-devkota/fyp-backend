from django.urls import path
from .views import GetUserFromJWT, UserTransactions,LoadFunds,GetFunds, DashboardView,WishlistStock,GetWishList,RemoveFromWishlistView
urlpatterns = [
        path("info/", GetUserFromJWT.as_view(), name="get_user_from_jwt"),
        path("transactions/", UserTransactions.as_view(), name="user_transactions"),
        path("load-funds/", LoadFunds.as_view(), name="load_funds"),
        path("get-funds/", GetFunds.as_view(), name="get_funds"),	
        path("dashboard/", DashboardView.as_view(), name="dashboard"),
        path("wishlist/add/", WishlistStock.as_view(), name="wishlist_stock"),
        path("wishlist/list/", GetWishList.as_view(), name="wishlist_stock"),
        path("wishlist/remove/<str:symbol>/", RemoveFromWishlistView.as_view(), name="remove_from_wishlist"),
]

