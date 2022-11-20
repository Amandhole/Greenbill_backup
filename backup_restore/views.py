import mimetypes
import os
import sweetify
import shutil

from django.core import management
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.management import call_command
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views import is_owner

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def backup(request):
    if request.method == "POST":
        dir_path = os.path.join(settings.MEDIA_ROOT, 'backup')
        dir_path_sqlite = os.path.join(settings.MEDIA_ROOT, 'backup_sqlite')
        try:
            shutil.rmtree(dir_path)
            call_command('dbbackup')
            # files = ['db.sqlite3']
            # for f in files:
            #     shutil.copy(f, dir_path_sqlite)
            sweetify.success(request, title="Success", icon='success', text='Backup Created Successfully.', timer=1500)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
            sweetify.success(request, title="error", icon='error',
                             text='Failed to create Backup.', timer=1500)

        return redirect("/create-database-backup/")

    else:
        dir_path = os.path.join(settings.MEDIA_ROOT, 'backup')
        list_data = os.listdir(dir_path)

        database_file = list_data[0]
        context = {
            'database_file': database_file,
            "SettingsNavclass": "active",
            "settingsCollapseShow": "show",
            "backupRestoreActiveClass": "active"
        }
        return render(request, "super_admin/backup_restore.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def download_file(request):
    # fill these variables with real values
    dir_path = os.path.join(settings.MEDIA_ROOT, 'backup')
    list_data = os.listdir(dir_path)

    filename = list_data[0]

    fl = open(os.path.join(dir_path, filename), 'r', encoding="utf-8")

    mime_type, _ = mimetypes.guess_type(dir_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/login/")
def database_restore(request):
    dir_path = os.path.join(settings.MEDIA_ROOT, 'backup')

    try:
        call_command('dbrestore')
        sweetify.success(request, title="Success", icon='success',
                         text='Database restore completed successfully.', timer=1500)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
        sweetify.success(request, title="Error", icon='error',
                         text='Failed to restore database.', timer=1500)

    return redirect("/create-database-backup/")
