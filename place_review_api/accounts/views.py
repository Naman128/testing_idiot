from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
)

User = get_user_model()


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    Creates a new user and returns an authentication token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user with name, phone number, and password.",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully.",
                        "token": "abc123xyz...",
                        "user": {"id": 1, "name": "John Doe", "phone_number": "9876543210"}
                    }
                }
            ),
            400: "Bad Request - Invalid input data"
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'User registered successfully.',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    Authenticates user and returns an authentication token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login with phone number and password to get authentication token.",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful.",
                        "token": "abc123xyz...",
                        "user": {"id": 1, "name": "John Doe", "phone_number": "9876543210"}
                    }
                }
            ),
            400: "Bad Request - Invalid credentials"
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Login successful.',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    API endpoint for user logout.
    Deletes the user's authentication token.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout and invalidate the authentication token.",
        responses={
            200: openapi.Response(
                description="Logout successful",
                examples={"application/json": {"message": "Logout successful."}}
            ),
            401: "Unauthorized - Token required"
        },
        tags=['Authentication']
    )
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass
        
        return Response({
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    API endpoint for viewing/updating user profile.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the current user's profile information.",
        responses={
            200: UserSerializer,
            401: "Unauthorized - Token required"
        },
        tags=['User Profile']
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update the current user's profile (partial update).",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad Request - Invalid data",
            401: "Unauthorized - Token required"
        },
        tags=['User Profile']
    )
    def patch(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
