import datetime
from django.db import models
from django.contrib.auth.models import User

class Joints(models.Model):
    name = models.CharField(max_length=225, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.ForeignKey('States', null=True, blank=True)
    zip = models.CharField(max_length=33, blank=True)
    country = models.CharField(max_length=150, blank=True)
    url = models.CharField(max_length=765, blank=True)
    phone = models.CharField(max_length=45, blank=True)
    fax = models.CharField(max_length=45, blank=True)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)
    chain = models.BooleanField(null=False, blank=False)
    notes = models.TextField(blank=True)
    open = models.BooleanField(default=True, blank=True)
    
    class Meta:
        db_table = u'joints'
        ordering = ['name']
        verbose_name_plural = "Joints"
        
    def __unicode__(self):
        return self.name

class SearchLogs(models.Model):
    query = models.CharField(max_length=165, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(max_length=45, blank=True)
    
    class Meta:
        db_table = u'search_logs'
        verbose_name_plural = "Search Logs"
    
    def __unicode__(self):
        return self.query

class States(models.Model):
    name = models.CharField(max_length=96)
    state_abbr = models.CharField(max_length=24, blank=True)
    
    class Meta:
        db_table = u'states'
        ordering = ['name']
        verbose_name_plural = "States"
        
    def __unicode__(self):
        return self.state_abbr

class Reviews(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    joint = models.ForeignKey(Joints)
    review = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)
    visible = models.BooleanField(default=True)
    
    class Meta:
        db_table = u'reviews'
        ordering = ['modified']
        verbose_name_plural = "Reviews"
        
    def __unicode__(self):
        return self.review

