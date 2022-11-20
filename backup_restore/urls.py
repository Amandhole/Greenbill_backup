from django.urls import path, include  # add this
from backup_restore import views
from django.contrib import admin

urlpatterns = [
    path("create-database-backup/", views.backup, name="create-database-backup"),
    path("download-database-backup/", views.download_file, name="download-database-backup"),
    path("database-restore/", views.database_restore, name="database-restore"),

] 