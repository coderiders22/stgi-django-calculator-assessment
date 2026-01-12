from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .authentication import CsrfExemptSessionAuthentication


# =========================
# CSRF COOKIE
# =========================
@method_decorator(ensure_csrf_cookie, name="dispatch")
class CSRFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "CSRF cookie set"})


# =========================
# REGISTER
# =========================
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        request.session.save()

        return Response({
            "message": "Registered & logged in successfully",
            "username": user.username
        })


# =========================
# LOGIN
# =========================
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        login(request, user)
        request.session.save()

        return Response({
            "message": "Login successful",
            "username": user.username,
            "is_authenticated": True
        })


# =========================
# LOGOUT (🔥 FIXED)
# =========================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        logout(request)
        request.session.flush()
        return Response({"message": "Logged out successfully"})


# =========================
# AUTH STATUS
# =========================
class MeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "is_authenticated": True,
                "username": request.user.username
            })
        return Response({"is_authenticated": False})
