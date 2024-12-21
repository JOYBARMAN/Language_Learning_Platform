"""Some serializer validator"""

from django.core.exceptions import ValidationError


class SixDigitOTPValidator:
    def __call__(self, value):
        if len(str(value)) != 6:
            raise ValidationError("OTP must be exactly 6 digits.")
