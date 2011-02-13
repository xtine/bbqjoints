from joints.models import Joints
from joints.models import SearchLogs
from django.contrib import admin

class JointsAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state')
admin.site.register(Joints, JointsAdmin)


class SearchLogsAdmin(admin.ModelAdmin):
    list_display = ('query', 'ip', 'date')
admin.site.register(SearchLogs, SearchLogsAdmin)
