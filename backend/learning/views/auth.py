from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from learning.serializers.auth import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    """POST /api/auth/register/ — creates a user and logs them in immediately."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)}, status=201
        )


class MeView(APIView):
    """GET /api/auth/me/ — the current user's identity, for the Profile tab."""

    def get(self, request):
        return Response(UserSerializer(request.user).data)
