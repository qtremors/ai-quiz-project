from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserCreationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from .models import User

# --- Helper function to get user from session ---
def get_user_from_session(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    return None

# --- Page Views ---
def home(request):
    user = get_user_from_session(request)
    return render(request, 'landing.html', {'user': user})

def setup(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    return render(request, 'setup.html', {'user': user})

def quiz(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    return render(request, 'quiz.html', {'user': user})

def results(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    return render(request, 'results.html', {'user': user})

# --- Auth Views ---
def signup_view(request):
    user = get_user_from_session(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form, 'user': user})

def login_view(request):
    user = get_user_from_session(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_to_login = User.objects.get(email=email)
            request.session['user_id'] = user_to_login.id
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'user': user})

def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('home')

def settings_view(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')

    # Initialize forms
    account_form = UpdateAccountForm(instance=user)
    password_form = ChangePasswordForm(user=user)

    if request.method == 'POST':
        # Check which form was submitted based on the submit button's name
        if 'update_account' in request.POST:
            account_form = UpdateAccountForm(request.POST, instance=user)
            if account_form.is_valid():
                account_form.save()
                messages.success(request, 'Your account details have been updated!')
                return redirect('settings')
        
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(user=user, data=request.POST)
            if password_form.is_valid():
                user.password = make_password(password_form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('settings')

    context = {
        'user': user,
        'account_form': account_form,
        'password_form': password_form
    }
    return render(request, 'settings.html', context)

