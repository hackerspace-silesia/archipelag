from django.contrib import admin
from archipelag.event_log.models import EventLog

# Register your models here.

class EventLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(EventLog, EventLogAdmin)
