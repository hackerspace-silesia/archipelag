from django.contrib import admin
from archipelag.share_log.models import ShareLog

# Register your models here.

class ShareLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(ShareLog, ShareLogAdmin)
