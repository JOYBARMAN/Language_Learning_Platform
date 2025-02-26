# Generated by Django 5.1.4 on 2025-01-07 18:35

import dirtyfields.dirtyfields
import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('title', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/course')),
                ('image_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('video_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('actual_price', models.FloatField(default=0)),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('skill_level', models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced'), ('EXPERT', 'Expert'), ('ALL', 'All')], default='ALL', max_length=100)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('certificate', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='YES', max_length=100)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
            options={
                'verbose_name': 'Course Detail',
                'verbose_name_plural': 'Course Details',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
            options={
                'verbose_name': 'Course Lesson',
                'verbose_name_plural': 'Course Lessons',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseLessonLecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('course_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courselesson')),
            ],
            options={
                'verbose_name': 'Course Lesson Lecture',
                'verbose_name_plural': 'Course Lesson Lectures',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('review', models.TextField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Course Review',
                'verbose_name_plural': 'Course Reviews',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ListTypeDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('text', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('REQUIREMENTS', 'Requirements'), ('LEARNING_OUTCOMES', 'Learning Outcomes'), ('UNDEFINED', 'Undefined')], default='UNDEFINED', max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
            options={
                'verbose_name': 'List Type Description',
                'verbose_name_plural': 'List Type Descriptions',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('payment_status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('REFUNDED', 'Refunded'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=100)),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('completed_lecture', models.ManyToManyField(blank=True, to='courses.courselessonlecture')),
            ],
            options={
                'verbose_name': 'Course Enrollment',
                'verbose_name_plural': 'Course Enrollments',
                'constraints': [models.UniqueConstraint(fields=('course', 'user'), name='unique_course_enrollment')],
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
