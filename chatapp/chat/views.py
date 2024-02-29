from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions

from .forms import SignUpForm, UserUpdateForm, AccountUpdateForm

from . import models
from . import serializers


# Create your views here.

@login_required
def index(request):
    users = User.objects.all().exclude(pk=request.user.id)
    return render(request, 'index.html', {"users": users})


@login_required
def room(request, room_name):
    room_object = models.Room.objects.filter(room_name=room_name).first()
    chats = []

    if room_object:
        chats = models.Message.objects.filter(room=room_object)
    else:
        room_object = models.Room(room_name=room_name)
        room_object.save()

    return render(request, "room.html", {"room_name": room_name, 'chats': chats})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('/accounts/login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        account_update_form = AccountUpdateForm(request.POST,
                                                request.FILES,
                                                instance=request.user.account)
        if user_update_form.is_valid() and account_update_form.is_valid():
            user_update_form.save()
            account_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account')  # Redirect back to profile page

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        account_update_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'user_update_form': user_update_form,
        'account_update_form': account_update_form
    }

    return render(request, 'account.html', context)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAdminUser]
