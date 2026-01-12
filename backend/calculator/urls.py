# calculator/urls.py
from django.urls import path

from .auth_views import (
    CSRFView,
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
)

from .views import (
    CalculateView,
    HistoryView,
    clear_history,
    delete_history_item,
)

urlpatterns = [
    # ================= AUTH =================
    path("auth/csrf/", CSRFView.as_view(), name="csrf"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", MeView.as_view(), name="me"),

    # ================= CALCULATOR =================
    path("calculate/", CalculateView.as_view(), name="calculate"),
    path("history/", HistoryView.as_view(), name="history"),
    path("history/clear/", clear_history, name="clear-history"),
    path("history/<int:pk>/", delete_history_item, name="delete-history"),
]
