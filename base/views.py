import re
from turtle import up
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Tourney, Sport, Message
from .forms import TourneyForm, UserForm

""" tournies = [
    {'id' : 1, 'name' : 'First tennis tourney!!!'},
    {'id' : 2, 'name' : 'Second tennis tourney!!!'},
    {'id' : 3, 'name' : 'Third tennis tourney!!!'}
] """

# Create your views here.

def loginUser(request) :
    page = 'login'
    if request.user.is_authenticated :
        return redirect('home')

    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'Username OR password does not exist!')

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request) :
    logout(request)
    return redirect('home')

def registerUser(request) :
    if request.method == 'POST' :
        registerForm = UserCreationForm(request.POST)
        if registerForm.is_valid() :
            user = registerForm.save()
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'An error occured during registration!')

    registerForm = UserCreationForm()
    context = {'form' : registerForm}
    return render(request, 'base/login_register.html', context)

def userProfile(request, pk) :
    user = User.objects.get(id=pk)
    tournies = user.tourney_set.all()
    comments = user.message_set.all()
    sports = Sport.objects.all()
    context = {'user' : user, 'tournies' : tournies, 'comments' : comments, 'sports' : sports}
    return render(request, 'base/user_profile.html', context)

def home(request) :
    q = request.GET.get('q') if request.GET.get('q') else ''
    tournies = Tourney.objects.filter(
        Q(sport__sport__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
        )
    sports = Sport.objects.all()
    tourney_count = tournies.count()
    comments = Message.objects.filter(
        Q(tourney__sport__sport__icontains=q)
    )
    context = {'tournies' : tournies, 'sports' : sports, 'tourney_count' : tourney_count, 
                'comments' : comments}
    return render(request, 'base/home.html', context)

def tourney(request, pk) :
    tourney = None
    tourney = Tourney.objects.get(id = pk)

    if request.method == 'POST' :
        message = Message.objects.create(
            user = request.user,
            tourney = tourney,
            body = request.POST.get('body'),
        )
        tourney.participants.add(request.user)
        return redirect('tourney', pk=tourney.id)

    participants = tourney.participants.all()
    comments = tourney.message_set.all().order_by('-created')
    context = {'tourney' : tourney, 'comments' : comments, 'participants' : participants}
    return render(request, 'base/tourney.html', context)

@login_required(login_url='user-login')
def createTourney(request) :
    if request.method == 'POST' :
        form = TourneyForm(request.POST)
        if form.is_valid() :
            tourney = form.save(commit=False)
            tourney.host = request.user
            tourney.save()
            return redirect('home')

    form = TourneyForm()
    context = {'form' : form}
    return render(request, 'base/tourney_form.html', context)

@login_required(login_url='user-login')
def updateTourney(request, pk) :
    tourney = Tourney.objects.get(id = pk)

    if request.user != tourney.host :
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST' :
        updatedForm = TourneyForm(request.POST, instance=tourney)
        if updatedForm.is_valid() :
            updatedForm.save()
            return redirect('home')

    tourneyForm = TourneyForm(instance=tourney)
    context = {'form' : tourneyForm}

    return render(request, 'base/tourney_form.html', context)

@login_required(login_url='user-login')
def deleteTourney(request, pk) :
    
    tourney = Tourney.objects.get(id = pk)

    if request.user != tourney.host :
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST' :
        tourney.delete()
        return redirect('home')
    
    context = {'obj' : tourney}
    return render(request, 'base/delete.html', context)


@login_required(login_url='user-login')
def deleteMessage(request, pk) : 
    
    message = Message.objects.get(id = pk)

    if request.user != message.user :
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST' :
        message.delete()
        return redirect('home')
    
    context = {'obj' : message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='user-login')
def updateUser(request) :
    user = request.user

    if request.method == 'POST' :
        form = UserForm(request.POST, instance=user)
        if form.is_valid() :
            form.save()
            return redirect('user-profile', pk=user.id)

    form = UserForm(instance=user)
    context = {'form' : form}
    return render(request, 'base/update_user.html', context)