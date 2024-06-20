from django.urls import path
from . import views  # Certifique-se de que o import está correto

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file_root'),
    path('upload/<int:folder_id>/', views.upload_file, name='upload_file'),  # Rota para upload com folder_id
    path('download/<int:file_id>/', views.download_file, name='download_file'),  # Rota para download
    path('logout/', views.logout, name='logout'),  # Rota para logout
]
