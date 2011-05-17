from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from joints.models import Joints, States, Reviews

import datetime

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
    
def joint(request, joint_id):
    try:
        j = Joints.objects.get(pk=joint_id)
        s = States.objects.get(state_abbr=j.state)
    except Joints.DoesNotExist:
        raise Http404
    # Get reviews
    try:
        reviews = Reviews.objects.filter(joint=joint_id)
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
    try :
        p = request.POST
        request.POST['rating']
        try: # If User already has review, grab primary key for update
            user_review = Reviews.objects.get(user=request.user.id, joint=joint_id)
            user_pk = user_review.id
            user_created = user_review.created
        except: # Otherwise create a new entry
            user_pk = None
            user_created = datetime.datetime.now()
            
        Reviews(pk=user_pk, joint_id=joint_id, user_id=request.user.id, rating=p['rating'], review=p['review'], created = user_created, updated = datetime.datetime.now()).save()

        return HttpResponseRedirect(reverse('joints.views.joint', args=(j.id,)))        
            
    except:
        return render_to_response('joint.html', {
            'joint': j,
            'state' : s,
            'reviews': reviews,
            'error_message': "You didn't rate the joint.",
        }, context_instance=RequestContext(request))   
        

