from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate





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
       
    return HttpResponse({username,email,password})

    #Anchor else 

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            return HttpResponse('autenticado')
        else:
            return HttpResponse('Email ou Password estão inválidos, por favor tente novamente! Obrigado!')