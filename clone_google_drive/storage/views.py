from typing import List
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import ModelWithFileField, Folder
import os
from django.contrib.auth import logout as auth_logout
from django.conf import settings

@login_required
def upload_file(request, folder_id: int | None = None):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user  # Atribui o usuário autenticado ao campo 'user'
            
            if folder_id:
                this_folder = get_object_or_404(Folder, id=folder_id)
                instance.folder = this_folder  # Define a pasta onde o arquivo será salvo
            instance.save()

            if folder_id:
                return HttpResponseRedirect(reverse('upload_file', args=[folder_id]))  # Redireciona para a página de upload da pasta atual

            return HttpResponseRedirect(reverse('upload_file_root'))
    
    elif request.method == 'GET':
        form = UploadFileForm()

    # Coletar todos os arquivos do folder para o user
    user = request.user
    this_folder = Folder.objects.filter(
        id=folder_id,
    ).first()

    files = ModelWithFileField.objects.filter(
        user=user,
        folder=this_folder,
    )
    
    # Coletar todos os folders do folder para o user
    child_folders = Folder.objects.filter(
        parent=this_folder
    )

    # Template upload.html precisa de user, folder_id, child_folders, form, files
    return render(
        request=request,
        template_name="upload.html",
        context={
            "user": user, 
            "folder_id": folder_id, 
            "child_folders": child_folders, 
            "form": form,
            "files": files,
        }
    )


    

@login_required
def download_file(request, file_id):
    file_instance = get_object_or_404(ModelWithFileField, id=file_id)
    file_path = file_instance.file_field.path
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

def logout(request):
    auth_logout(request)
    return redirect('login')
