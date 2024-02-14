from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message, User, ImageMessage, Status, Comment
from .forms import RoomForm, UserForm, MyUserCreationForm, ImageMessageForm, PdfMessageForm, StatusForm, CommentForm
from itertools import chain


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        try:
            if request.user.is_authenticated():
                return redirect('home')
        except:
            pass

        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            pass
        except:
            messages.error(request, 'Invalid username!')
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid password!')


    context = {'page': page}
    return render(request, 'base/login_register.html', context=context)

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred while registering!')
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('home')

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages
    }
    return render(request, 'base/home.html', context=context)

def room(request, pk):
    # room = Room.objects.get(id=pk)
    # room_messages = room.message_set.all().order_by('-created')
    # participants = room.participants.all()
    # if request.method == 'POST':
    #     message = Message.objects.create(
    #         user=request.user,
    #         room=room,
    #         body=request.POST.get('body')
    #     )
    #     room.participants.add(request.user)
    #     return redirect('room', pk=room.id)
    # context = {
    #     'room': room,
    #     'room_messages': room_messages,
    #     'participants': participants,
    # }
    # return render(request, 'base/room.html', context=context)


    room = Room.objects.get(id=pk)
    # room_messages = room.message_set.all().order_by('-created')
    room_messages = room.message_set.all()
    image_messages = room.imagemessage_set.all()
    pdf_messages = room.pdfmessage_set.all()
    participants = room.participants.all()

    # Merge and order the messages
    all_messages = sorted(
        chain(room_messages, image_messages, pdf_messages),
        key=lambda message: message.created,
        reverse=True
    )

    if request.method == 'POST':
        print("==============================")
        print(request.POST)
        print(request.FILES)
        print("==============================")
        if 'body' in request.POST:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
        elif 'pdf_file' in request.FILES:
            form = PdfMessageForm(request.POST, request.FILES)
            print("==============================")
            print("ACEPTING : PDF")
            print("==============================")
            if form.is_valid():
                pdf_message = form.save(commit=False)
                pdf_message.user = request.user
                pdf_message.room = room
                pdf_message.save()
                room.participants.add(request.user)
            else:
                messages.error(request, 'Only PDF files are allowed to upload.')
                print("Form Errors:", form.errors)
                print("Cleaned Data:", form.cleaned_data)
                print("ERROR WHILE UPLOADING................................................................")
        else:
            form = ImageMessageForm(request.POST, request.FILES)
            if form.is_valid():
                image_message = form.save(commit=False)
                image_message.user = request.user
                image_message.room = room
                image_message.save()
                room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'all_messages': all_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context=context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
        
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context=context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room.')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context=context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context=context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    # message = Message.objects.get(id=pk)
    message = Message.objects.filter(id=pk).first() or ImageMessage.objects.filter(id=pk).first()
    if message is None:
        return HttpResponse('Message not found')
    room_id = message.room.id
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room_id)
    context = {'obj': message}
    return render(request, 'base/delete.html', context=context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }

    return render(request, 'base/profile.html', context=context)


def updateUser(request):
    form = UserForm(instance=request.user)
    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)
    return render(request, 'base/update_user.html', context=context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context=context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context=context)


# Implementing status

@login_required(login_url='login')
def status(request):
    # Calculate the time threshold (24 hours ago)
    threshold = timezone.now() - timezone.timedelta(hours=24)

    # Delete status objects created before the threshold
    Status.objects.filter(created__lt=threshold).delete()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.save()
            return redirect('status')
    statuses = Status.objects.all()
    form = StatusForm()
    context = {'statuses': statuses, 'form': form}
    return render(request, 'base/status.html', context=context)

@login_required(login_url='login')
def status_delete(request, status_id):
    status = get_object_or_404(Status, id=status_id)

    # Check if the requesting user is the owner of the status
    if status.user == request.user:
        status.delete()
    
    # Redirect back to the status page
    return redirect('status')


@login_required(login_url='login')
def like_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)

    if request.user not in status.liked_by.all():
        status.liked_by.add(request.user)
        messages.success(request, 'Status liked.')
    else:
        status.liked_by.remove(request.user)
        messages.success(request, 'Status unliked.')

    return redirect('status')



def current_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    if request.method == 'POST':
        if 'body' in request.POST:
            Comment.objects.create(status=status, text=request.POST['body'], user=request.user)
    comments = Comment.objects.filter(status=status)
    context = {'status': status, 'comments': comments}

    return render(request, 'base/current_status.html', context=context)

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    status_id = comment.status.id

    # Check if the requesting user is the owner of the status
    if comment.user == request.user:
        comment.delete()
    
    # Redirect back to the status page
    return redirect(reverse('current_status', args=[status_id]))

def likes_of_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    liked_by = status.liked_by.all()
    context = {'liked_by': liked_by, }
    return render(request, 'base/current_status_likes.html', context=context)