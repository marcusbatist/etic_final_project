from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com esse username!!')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponse({username, email, password})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('upload_file'))  # Redireciona para a página de upload
            
        return HttpResponse('Email ou Password estão inválidos, por favor tente novamente! Obrigado!')
    return render(request, 'login.html')
