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
def upload_file(request, folder_id: int | None):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user  # Atribui o usuário autenticado ao campo 'user'
            
            if folder_id:
                folder = get_object_or_404(Folder, id=folder_id)
                instance.folder = folder  # Define a pasta onde o arquivo será salvo
            instance.save()

            # Cria a pasta se não existir
            full_folder_path = os.path.join(settings.MEDIA_ROOT, str(folder_id))
            os.makedirs(full_folder_path, exist_ok=True)
           
            return HttpResponseRedirect(reverse('upload_file', args=[folder_id]))  # Redireciona para a página de upload da pasta atual
    else:
        form = UploadFileForm()

    folder_user_files = ModelWithFileField.objects.filter(folder=folder_id, user=request.user)
    path_list = []
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id)
        while folder:
            path_list.insert(0, folder)
            folder = folder.parent  

    subfolders = Folder.objects.filter(parent=folder_id)

    return render(request, 'upload.html', {
        'form': form,
        'folder_id': folder_id,
        'files': folder_user_files,
        'path_list': path_list,
        'subfolders': subfolders,
    })

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
