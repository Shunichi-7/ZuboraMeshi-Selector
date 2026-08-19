from django.contrib import admin

# Register your models here.

from .models import Recipe, Favorite

admin.site.register(Recipe)

admin.site.register(Favorite) # お気に入り機能を管理画面で管理できるようにする

