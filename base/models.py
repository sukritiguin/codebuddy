from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from uuid import uuid4
import uuid
import os

def validate_pdf_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File type is not supported. Please upload a PDF file.')


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated', '-created']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    
    class Meta:
        ordering = ['-updated', '-created']


# 2nd Part start here
class ImageMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Define a function to generate unique filenames
    def unique_image_filename(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('chat_images/', unique_filename)
    image = models.ImageField(upload_to=unique_image_filename)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image by {self.user.username} in {self.room.name}"
    
    class Meta:
        ordering = ['-updated', '-created']


class PdfMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    def unique_pdf_filename(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('pdf_files/', unique_filename)
    pdf_file = models.FileField(upload_to=unique_pdf_filename, validators=[validate_pdf_extension])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PDF uploaded by {self.user.username} in {self.room.name}"

    class Meta:
        ordering = ['-updated', '-created']



class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_statuses', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.created.strftime} : {"Status"}'
    
    class Meta:
        ordering = ('-created',)
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.status}'

    class Meta:
        ordering = ('-created',)