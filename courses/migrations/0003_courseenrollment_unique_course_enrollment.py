# Generated by Django 5.1.4 on 2025-01-06 17:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_courselesson_courselessonlecture_courseenrollment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='courseenrollment',
            constraint=models.UniqueConstraint(fields=('course', 'user'), name='unique_course_enrollment'),
        ),
    ]
