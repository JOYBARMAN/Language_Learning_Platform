from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
