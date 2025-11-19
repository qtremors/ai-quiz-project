from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Avg
from .forms import SignUpForm, LoginForm, UserUpdateForm 
from apps.quizzes.models import Quiz

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto-login after signup
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    """
    Shows quiz history and statistics.
    """
    user_quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate Stats
    total_quizzes = user_quizzes.count()
    avg_score = user_quizzes.aggregate(Avg('score'))['score__avg'] or 0
    
    context = {
        'quizzes': user_quizzes,
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 1)
    }
    return render(request, 'users/dashboard.html', context)



@login_required
def account_settings(request):
    # Initialize forms with current user instance
    profile_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        
        if 'update_profile' in request.POST:
            profile_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('account_settings')
            else:
                messages.error(request, 'Error updating profile.')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                login(request, user) # Keep user logged in
                messages.success(request, 'Password changed successfully!')
                return redirect('account_settings')
            else:
                messages.error(request, 'Error changing password.')

    # Apply styles
    for field in password_form.fields.values():
        field.widget.attrs.update({'class': 'form-input'})

    return render(request, 'users/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })