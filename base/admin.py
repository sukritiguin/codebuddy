from django.contrib import admin
from .models import Room, Topic, Message, User, ImageMessage, PdfMessage, Status, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(ImageMessage)
admin.site.register(PdfMessage)
admin.site.register(Status)
admin.site.register(Comment)