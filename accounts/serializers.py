from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from cycle import settings

from products.serializers import ProductSerializer
from reviews.serializers import FavoriteProductSerializer
from products.models import Product
from .tasks import send_activation_mail, send_restore_password_mail

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already exists')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        return super().validate(attrs)

    def create(self):
        user = User.objects.create_user(**self.validated_data)
        user.create_activation_code()
        send_activation_mail.delay(user.email, user.activation_code)
        # user.send_activation_code()


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email does not exists')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Password is not valid')
        return super().validate(attrs)


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email does not exists')
        return email

    def send_verification_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_restore_password_mail.delay(email, user.activation_code)
        # send_mail(
        #     subject='Activation',
        #     message=f'?????? ?????? {user.activation_code}',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[email],
        #     fail_silently=False
        # )


class RestorePasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=20, min_length=20)
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('activation_code')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User with this email and activation code not found')
        return super().validate(attrs)

    def set_new_password(self):
        print(self.validated_data)
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4)
    new_password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
        return password

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        password_confirm = attrs.get('password_confirm')
        if new_password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        return super().validate(attrs)

    def set_new_password(self):
        user = self.context['request'].user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        email = representation['email']
        serializer = ProductSerializer(instance.user.all(),
                                       many=True, context=self.context)
        favorite = FavoriteProductSerializer(instance.favorite.filter(user=email), many=True)
        representation['products'] = serializer.data
        favorite_list = []
        for product in favorite.data:
            favorite_list.append(
                ProductSerializer(Product.objects.get(id=product['product']), context=self.context).data)
        representation['favorite'] = favorite_list
        return representation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        serializer = ProductSerializer(instance.user.all(),
                                       many=True, context=self.context)
        representation['products'] = serializer.data
        return representation


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = User
        fields = ['email', 'image', 'phone_number']

    def validate_phone_number(self, phone_number):
        print(len(phone_number))
        if not 7 < len(phone_number) < 12:
            raise serializers.ValidationError('Not valid phone number')
        if not phone_number.isdigit():
            raise serializers.ValidationError('Phone number should only contain digits')
        return phone_number

