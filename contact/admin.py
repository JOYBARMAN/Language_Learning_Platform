from django.contrib import admin

from .models import (
    Contact,
    NewsLetter,
)

admin.site.register(Contact)
admin.site.register(NewsLetter)