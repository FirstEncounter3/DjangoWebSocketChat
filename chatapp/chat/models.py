from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='media', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Account'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pic = Image.open(self.avatar.path)

        if pic.height > 300 or pic.width > 300:
            output_size = (300, 300)
            pic.thumbnail(output_size)  # Resize image
            pic.save(self.avatar.path)


class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.room)
