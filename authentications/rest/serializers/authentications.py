"""Serializer for authentication"""

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers

from core.models import User, UserOtp
from core.choices import OtpType
from core.utils import (
    is_valid_bd_phone_num,
    send_otp_to_user,
    send_email_for_password_reset,
    get_tokens_for_user,
)

from .validators import SixDigitOTPValidator


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=8, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=8, required=True
    )

    class Meta:
        model = User
        fields = [
            "phone",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "password",
            "confirm_password",
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone(self, value):
        if value and not is_valid_bd_phone_num(value):
            raise serializers.ValidationError(
                "This is not a valid Bangladeshi phone number "
            )
        return value

    def validate_password(self, value):
        confirm_password = self.initial_data.get("confirm_password", "")

        if value != confirm_password:
            raise serializers.ValidationError(
                "password and confirm password do not match."
            )

        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create(**validated_data)
        token = get_tokens_for_user(user)
        send_otp_to_user(user=user, otp_type=OtpType.REGISTRATION)
        return {
            "messages": "Registration Successful. OTP send to your mail please activate your account.",
            "token": token,
        }


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(style={"input_type": "password"}, required=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return {"messages": "Login Successful", "token": token}
        else:
            raise serializers.ValidationError(
                {"non_field_errors": "Email or Password is not valid"}
            )


class ActivateAccountSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField(validators=[SixDigitOTPValidator()])

    class Meta:
        model = UserOtp
        fields = ["otp"]

    def create(self, validated_data):
        request = self.context["request"]
        user_otp = self.Meta.model.objects.get(user=request.user)

        if validated_data["otp"] != user_otp.otp:
            raise serializers.ValidationError({"otp": "Invalid OTP."})
        elif user_otp.is_expired():
            raise serializers.ValidationError({"otp": "OTP Expired."})
        else:
            user_otp.is_activated = True
            user_otp.save()

            return {"messages": "Your account has been successfully activated."}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, min_length=8, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    class Meta:
        fields = [
            "old_password",
            "new_password",
            "confirm_password",
        ]

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password")

        return value

    def validate_new_password(self, value):
        confirm_password = self.initial_data.get("confirm_password", "")

        if value != confirm_password:
            raise serializers.ValidationError(
                "new password and confirm password do not match."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        new_password = validated_data.get("new_password")

        # Use set_password to update and hash the new password
        user.set_password(new_password)
        user.save()

        return {"messages": "Your password has been changed successfully."}


class PasswordResetMailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    class Meta:
        fields = ["email"]

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return {"email": value, "user": user}
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")

    def create(self, validated_data):
        email = validated_data["email"]["email"]
        user = validated_data["email"]["user"]
        token = PasswordResetTokenGenerator().make_token(user)
        link = f"http://localhost:8000/api/v1/auth/password-reset/{user.uid}/{token}"

        # send email for password reset
        send_email_for_password_reset(to_email=email, link=link)

        return {
            "messages": "Password reset link has been sent to your email. Please check it"
        }


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={"input_type": "password"}, min_length=8, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    class Meta:
        fields = [
            "new_password",
            "confirm_password",
        ]

    def validate_new_password(self, value):
        confirm_password = self.initial_data.get("confirm_password", "")

        if value != confirm_password:
            raise serializers.ValidationError(
                "new password and confirm password do not match."
            )

        return value

    def create(self, validated_data):
        password = validated_data.get("new_password")
        uid = self.context.get("uid")
        token = self.context.get("token")
        user = User.objects.get(uid=uid)

        # Check user token is valid or not
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("token is not valid or expired")

        user.set_password(password)
        user.save()

        return {"messages": "Your password has been changed successfully."}
