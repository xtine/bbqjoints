from content.models import Advertisement
from django.contrib import admin

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'topright', 'sidebar')


admin.site.register(Advertisement, AdvertisementAdmin)
