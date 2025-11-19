from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def languages_list(request):
    return render(request, 'core/languages.html')