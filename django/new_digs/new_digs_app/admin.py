from django.contrib import admin

from new_digs_app.models import MODELS

for model in MODELS:
    admin.site.register(model)
