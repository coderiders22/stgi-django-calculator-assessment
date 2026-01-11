# calculator/urls.py

from django.urls import path
from .views import (
    CalculateView,
    HistoryView,
    clear_history,
    delete_history_item
)
from .auth_views import (
    CSRFView,     
    RegisterView,
    LoginView,
    LogoutView,
    MeView
)
urlpatterns = [
    # --------------------
    # Calculator APIs
    # --------------------
    path("calculate/", CalculateView.as_view()),

    # History (user + guest)
    path("history/", HistoryView.as_view()),
    path("history/clear/", clear_history),

    # Delete single history (logged-in user only)
    path("history/<int:pk>/", delete_history_item),

    # --------------------
    # Auth APIs (SESSION BASED)
    # --------------------
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/me/", MeView.as_view()),  
    path("auth/csrf/", CSRFView.as_view()),
]
