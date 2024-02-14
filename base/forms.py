from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from .models import Room, User, ImageMessage, PdfMessage, Status, Comment

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2')


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'username' , 'bio', 'avatar']

# 2nd part start here
class ImageMessageForm(forms.ModelForm):
    class Meta:
        model = ImageMessage
        fields = ['image']

class PdfMessageForm(forms.ModelForm):
    class Meta:
        model = PdfMessage
        fields = ['pdf_file']

class StatusForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Status
        fields = ['text']

    
class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Comment
        fields = ['text']