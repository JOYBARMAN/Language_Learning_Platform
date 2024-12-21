# Generated by Django 5.1.4 on 2024-12-21 08:37

import dirtyfields.dirtyfields
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Unique identifier for this model instance.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp indicating when the instance was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp indicating when the instance was last updated.')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DELETED', 'Deleted'), ('DRAFT', 'Draft'), ('REMOVED', 'Removed')], default='ACTIVE', help_text='Status of the instance, typically used for soft deletion.', max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/department')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='categories.category')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
