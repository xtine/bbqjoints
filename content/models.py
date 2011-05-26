from django.db import models

class Advertisement(models.Model):
    topright = models.TextField()
    sidebar = models.TextField()
    
    class Meta:
        db_table = u'advertisements'
