from django.apps import apps, AppConfig
from django.contrib import admin


from django.contrib import admin
from django.apps import apps

post_models = apps.get_app_config('backend').get_models()

for model in post_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
