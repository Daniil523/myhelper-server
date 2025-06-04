from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer, LoginSerializer, RefreshSerializer, LogoutSerializer
from django.contrib.auth import authenticate, logout
from drf_spectacular.utils import extend_schema

@extend_schema(request=RegisterSerializer)
class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=LoginSerializer)
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(request=RefreshSerializer)
class RefreshAPI(APIView):
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(request=LogoutSerializer)
class LogoutAPI(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
       
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response_data = {
                "success": "Successfully logged out"
            }
            
            return Response(response_data, status=status.HTTP_205_RESET_CONTENT)
            
        except TokenError as e:
            return Response(
                {"error": "Invalid or expired token", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Logout failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )