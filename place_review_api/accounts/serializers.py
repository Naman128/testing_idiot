from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates phone_number uniqueness and creates a new user.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        help_text='Password must be at least 6 characters long.'
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'password']
        extra_kwargs = {
            'name': {'required': True},
            'phone_number': {'required': True},
        }

    def validate_phone_number(self, value):
        """
        Validate that the phone number is unique.
        """
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                'A user with this phone number already exists.'
            )
        return value

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid phone number or password.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid phone number or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for returning authentication token with user info.
    """
    token = serializers.CharField()
    user = UserSerializer()
