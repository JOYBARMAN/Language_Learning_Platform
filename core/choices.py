from django.db.models import TextChoices

class UserTypeChoices(TextChoices):
    ADMIN = "ADMIN", "Admin"
    AUTHOR = "AUTHOR", "Author"
    LEARNER = "LEARNER", "Learner"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"
    STAFF = "STAFF", "Staff"


class OtpType(TextChoices):
    REGISTRATION = "REGISTRATION", "Registration"
    LOGIN = "LOGIN", "Login"
    UNDEFINED = "UNDEFINED", "Undefined"

from django.db.models import TextChoices


class BloodGroups(TextChoices):
    NOT_SET = "NOT_SET", "Not Set"
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"


class UserGender(TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    OTHER = "OTHER", "Other"