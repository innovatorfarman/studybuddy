import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect") 
    data ={
        'page':page,
        }
    return render(request,'base/login_register.html',data)
      

# # Register

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
    data = {
        "form":form,
    }        
    return render(request,'base/login_register.html',data)
    

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()[0:5]
    if request.method =="GET":
        if 'q' in request.GET:
            q = request.GET['q'] if request.GET['q'] != None else ""
            rooms = Room.objects.filter( 
                Q(name__icontains=q) |
                Q(topic__name__icontains = q) |
                Q(description__icontains = q)
            )
    room_messages = Message.objects.all()
    room_count= rooms.count()
    data  = {
        'rooms':rooms,
        'topics':topics,
        'room_messages':room_messages,
        'room_count':room_count,
    }
    return render(request, 'base/home.html', data)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method =="POST":
        body = request.POST['body']
        Message.objects.create(
            user = request.user,
            room = room,
            body = body,
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

   
    data = {
    "room":room,
    "room_messages":room_messages,
    "participants":participants,

    }
    return render(request, 'base/room.html/',data)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST['name'],
            description = request.POST['description'],
        )
        return redirect('home')   
                       
    data={
        'form':form,
        'topics':topics,
    }
    return render(request, 'base/create-room.html',data)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return redirect('room',pk=room.id)

    if request.method=="POST":
        topic_name = request.POST['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name= request.POST['name']
        room.description= request.POST['description']
        room.save()
        return redirect('room',pk=room.id)
    data = {
        'form':form,
        'topics':topics,
    }
    return render(request, 'base/create-room.html', data)
    
@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return redirect('room',pk=room.id)
    if request.method=="POST":
        room.delete()
        messages.success(request, "Room deleted!")
        return redirect('home')
    data ={
        'obj':room, 
    }
    return render(request, 'base/delete.html',data)

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return redirect('home')
    if request.method == "POST":
        message.delete()
        messages.success(request,"Message deleted successfully!")
        return redirect('home')
    data={
        'obj':message,
    }

    return render(request,'base/delete.html',data)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    data={
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics,
        
    }
    return render(request,'base/user_profile.html',data)

@login_required(login_url='login')
def updateProfile(request):
    user=request.user
    form = UserForm(instance=user)    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
        else:
            messages.error(request,"Error while submitting form")
    data ={
        'form':form,
    }

    return render(request, 'base/edit-user.html',data)


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics=Topic.objects.filter(name__icontains = q)
    data ={
        'topics':topics,
    }
    return render(request,'base/topics.html',data)

def activity(request):
    room_messages = Message.objects.all()
    data={
        'room_messages':room_messages,
    }
    return render(request,'base/activity.html',data)
