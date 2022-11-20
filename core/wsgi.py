# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
