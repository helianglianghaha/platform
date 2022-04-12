import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QualityPlatform.settings")
django.setup()
from quality.view.API_version import API_function