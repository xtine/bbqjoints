from django.conf import settings
from content.models import Advertisement

def googleAnalytics(request):
    return {"googleAnalyticsID": settings.GOOGLE_ANALYTICS_ID}

def getAds(request):
    ads = Advertisement.objects.order_by('-pk')[0]
    return { 'ads' : ads }
