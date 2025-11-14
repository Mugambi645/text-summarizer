from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny


COOKIE_NAME = settings.REFRESH_COOKIE_NAME
COOKIE_SECURE = True  # set to True in production (HTTPS)
COOKIE_SAMESITE = "Lax"  # Lax is often good for SPA. Consider Strict if possible.
COOKIE_PATH = "/api/auth/"  # scope cookie to auth endpoints (optional)

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    On successful login, set the refresh token in an httpOnly cookie and return access token in response.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh = response.data.get("refresh")
            access = response.data.get("access")

            # set httpOnly cookie
            resp = Response({"access": access}, status=status.HTTP_200_OK)
            resp.set_cookie(
                key=COOKIE_NAME,
                value=refresh,
                httponly=True,
                secure=COOKIE_SECURE,
                samesite=COOKIE_SAMESITE,
                path=COOKIE_PATH,
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
            )
            return resp
        return response

class CookieTokenRefreshView(TokenRefreshView):
    """
    Use refresh cookie. The client calls /api/auth/refresh/ (cookie auto-sent).
    This view will rotate the refresh token if ROTATE_REFRESH_TOKENS is True.
    """
    def post(self, request, *args, **kwargs):
        # read refresh token from cookie, forward to parent logic using request.data
        refresh_token = request.COOKIES.get(COOKIE_NAME)
        if not refresh_token:
            return Response({"detail": "No refresh token cookie"}, status=status.HTTP_401_UNAUTHORIZED)

        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get("access")
            new_refresh = response.data.get("refresh")  # present if rotate enabled

            resp = Response({"access": access}, status=status.HTTP_200_OK)
            if new_refresh:
                resp.set_cookie(
                    key=COOKIE_NAME,
                    value=new_refresh,
                    httponly=True,
                    secure=COOKIE_SECURE,
                    samesite=COOKIE_SAMESITE,
                    path=COOKIE_PATH,
                    max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
                )
            return resp

        return response

class LogoutView(APIView):
    """
    Blacklist the refresh token (if present) and clear cookie.
    """
    def post(self, request):
        refresh_token = request.COOKIES.get(COOKIE_NAME)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # requires token_blacklist app
            except Exception:
                pass

        resp = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        resp.delete_cookie(COOKIE_NAME, path=COOKIE_PATH)
        return resp



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]