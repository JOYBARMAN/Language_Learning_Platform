"""Some utils function of core app"""

import re, random, os, logging

from django.core.mail import EmailMessage

from rest_framework_simplejwt.tokens import RefreshToken

from core.models import UserOtp

logger = logging.getLogger(__name__)


# Check phone number is valid or not
def is_valid_bd_phone_num(phone):
    # Define a regular expression pattern for a valid Bangladeshi phone number
    pattern = r"^\+?(88)?01[3-9]\d{8}$"

    # Use the re.match() function to check if the phone number matches the pattern
    return bool(re.match(pattern, phone))


# Generate otp for otp verificatio
def generate_otp():
    return random.randint(100000, 999999)


# Function for send mail
def send_email_for_otp(to_email, otp):
    subject = "OTP Verification for Language Learning Platform"
    body = f"Hello,\n\nYour OTP (One-Time Password) for account verification is: {otp}\n\nThank you for using Language Learning Platform."
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=os.environ.get("EMAIL_FROM"),
        to=[to_email],
    )
    try:
        email.send()
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"An error occurred while sending the email: {e}")


# Function for send otp to user
def send_otp_to_user(user, otp_type):
    user_otp, created = UserOtp.objects.get_or_create(user=user)
    # Generate and save OTP
    user_otp.otp = generate_otp()
    user_otp.otp_type = otp_type
    user_otp.save()

    # Send OTP via email
    send_email_for_otp(to_email=user_otp.user.email, otp=user_otp.otp)


# Function send email for password reset
def send_email_for_password_reset(to_email, link):
    subject = "Reset Your Password"
    body = f"Hello,\n\nWe received a request to reset your password for your account. To proceed with the password reset, click on the following link:\n\n{link}\n\nIf you did not request this password reset, please ignore this email.\n\nThank you for using Language Learning Platform."
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=os.environ.get("EMAIL_FROM"),
        to=[to_email],
    )
    try:
        email.send()
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"An error occurred while sending the email: {e}")


# Generate token munually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
