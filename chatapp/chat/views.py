from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UserUpdateForm, AccountUpdateForm

from . import models


# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


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
            return redirect('index')  # Redirect back to profile page

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        account_update_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'user_update_form': user_update_form,
        'account_update_form': account_update_form
    }

    return render(request, 'account.html', context)
    # return render(request, 'users/profile.html', context)

# class SignUp(CreateView):
#     model = models.Account
#     form_class = SignUpForm
#     success_url = '/accounts/login'
#     template_name = 'registration/signup.html'
