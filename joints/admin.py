from joints.models import Joints
# from joints.models import States
from django.contrib import admin

class JointsAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state')

admin.site.register(Joints, JointsAdmin)
# admin.site.register(States)