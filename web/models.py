import uuid

from django.db import models
from django.urls import reverse


class Audio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audio = models.FileField(upload_to='audios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    speaker_num = models.PositiveIntegerField(default=1)
    language = models.CharField(default="en-US", max_length=20)
    Enhanced_Model = (
        ('video', 'Video'),
        ('phone_call', 'Phone Call'),
    )
    model = models.CharField(choices=Enhanced_Model, default='video', help_text='select to enhance recognition result',
                             max_length=20)


class Transcript(models.Model):
    transcript = models.FileField(upload_to='transcripts/')
    audio = models.OneToOneField(Audio, on_delete=models.CASCADE, null=True)


class User(models.Model):
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])
