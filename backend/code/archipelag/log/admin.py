from django.contrib import admin
from archipelag.log.models import Log

# Register your models here.

class LogAdmin(admin.ModelAdmin):
    pass

admin.site.register(Log, LogAdmin)
