from joints.models import Joints
from joints.models import SearchLogs
from joints.models import Reviews
from django.contrib import admin

# dumb hack to get filtering working outside of sidebar for Django 1.2.4
# http://stackoverflow.com/questions/2065036/django-list-filter-and-foreign-key-fields
class SmarterModelAdmin(admin.ModelAdmin):
    valid_lookups = ()
    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup.startswith(self.valid_lookups):
            return True
        return super(SmarterModelAdmin, self).lookup_allowed(lookup, *args, **kwargs)

class JointsAdmin(SmarterModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'zip')
    
    valid_lookups = ('name')
        
    alphabet_filter = 'name'

class SearchLogsAdmin(admin.ModelAdmin):
    list_display = ('query', 'ip', 'date')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('review', 'rating', 'joint', 'user', 'modified', 'created', 'visible')

admin.site.register(SearchLogs, SearchLogsAdmin)
admin.site.register(Joints, JointsAdmin)
admin.site.register(Reviews, ReviewsAdmin)
