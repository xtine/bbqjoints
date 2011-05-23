from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from joints.models import Joints, States, Reviews

import datetime, urllib
from django.utils.html import strip_tags


def index(request):
    list_of_states = States.objects.all().order_by('name')
    context = RequestContext(request)
    return render_to_response('states_listing.html', {'list_of_states': list_of_states}, context_instance=context)

def state(request, state_abbr):
    try:
        j = Joints.objects.filter(state__state_abbr=state_abbr)
        s = States.objects.get(state_abbr=state_abbr)
    except Joints.DoesNotExist:
        raise Http404
    context = RequestContext(request)
    return render_to_response('state.html', {'joints': j, 'state': s}, context_instance=context)

def search(request):

    try:
        filterChains = request.GET['filterChains']
        filterChains = "AND chain = 0 "
    except:
        filterChains = ""

    try:
        query = request.GET['q']
        
        if query == '':
            error = "You have to enter a location to search for BBQ Joints."
            context = RequestContext(request)
            return render_to_response('search_results.html', {'error' : error}, context_instance=context)
        else:

            try:

                output = "csv"
                location = urllib.quote_plus(query)
                geocodeLookup = "http://maps.google.com/maps/geo?q=%s&output=%s" % (location, output)
                geocodeLookup = urllib.urlopen(geocodeLookup).read()
                geocode = geocodeLookup.split(',')

                print geocode[2], ", ", geocode[3]

                lat = geocode[2]
                lon = geocode[3]                

                # Haversine Formula for nearest points
                # Only show if the BBQ Joint is open
                # TODO: Filter by Chain
                j = Joints.objects.raw("SELECT id,  ( 3959 * acos( cos( radians(%s) ) * cos( radians( lat ) ) * cos( radians( lon ) - radians(%s) ) + sin( radians(%s) ) * sin( radians( lat ) ) ) ) AS distance FROM joints WHERE open = 1 %sHAVING distance < 50 ORDER BY distance LIMIT 0 , 11;" % (lat, lon, lat, filterChains))

            except: # Error if can't lookup geocode
                error = "The Search Function is not working right now, sorry."
                context = RequestContext(request)
                return render_to_response('search_results.html', {'error' : error}, context_instance=context)

            context = RequestContext(request)
            return render_to_response('search_results.html', {'query' : query, 'joints': j, 'lat' : lat, 'lon' : lon, 'filterChains' : filterChains}, context_instance=context)
    
    except:
        error = "You have to enter a location to search for BBQ Joints."
        context = RequestContext(request)
        return render_to_response('search_results.html', {'error' : error}, context_instance=context)
        

def joint(request, joint_id):
    try:
        j = Joints.objects.get(pk=joint_id)
        s = States.objects.get(state_abbr=j.state)
    except Joints.DoesNotExist:
        raise Http404
    # Get reviews
    try:
        reviews = Reviews.objects.filter(joint=joint_id, visible=True)
    except Reviews.DoesNotExist:
        reviews = None
    # Check if User has written a review already
    try:
        user_review = Reviews.objects.get(user=request.user.id, joint=joint_id)
    except Reviews.DoesNotExist:
        user_review = None
    context = RequestContext(request)
    return render_to_response('joint.html', {'joint': j, 'state': s, 'reviews': reviews, 'user_review':user_review }, context_instance=RequestContext(request))
    
def review(request, joint_id):
    j = get_object_or_404(Joints, pk=joint_id)
    s = get_object_or_404(States, state_abbr = j.state)
    
    try:
        reviews = Reviews.objects.filter(joint=joint_id)
    except Reviews.DoesNotExist:
        reviews = None
        
    try:
        user_review = Reviews.objects.get(user=request.user.id, joint=joint_id)
    except Reviews.DoesNotExist:
        user_review = None
        
    try :
        review = strip_tags(request.POST['review'])
        rating = request.POST['rating']
        
        if review:
        
            try: # If User already has review, grab primary key for update
                user_review = Reviews.objects.get(user=request.user.id, joint=joint_id)
                user_pk = user_review.id
                user_created = user_review.created
            except: # Otherwise create a new entry
                user_pk = None
                user_created = datetime.datetime.now()
            
            Reviews(pk=user_pk, joint_id=joint_id, user_id=request.user.id, rating=rating, review=review, created = user_created).save()

        else:
            return render_to_response('joint.html', {
                'joint': j,
                'state' : s,
                'reviews': reviews,
                'user_review': user_review,
                'error_message': "Can't submit without a review.",
            }, context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse('joints.views.joint', args=(j.id,)))

    except:
        return render_to_response('joint.html', {
            'joint': j,
            'state' : s,
            'reviews': reviews,
            'error_message': "Can't submit without a rating.",
        }, context_instance=RequestContext(request))


