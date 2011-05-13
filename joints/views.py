from joints.models import Joints, States, Reviews
from django.shortcuts import get_object_or_404, render_to_response

from django.template import RequestContext

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
    try:
        j = Joints.objects.get(pk=joint_id)
        s = States.objects.get(state_abbr=j.state)
        p = request.POST
        # If User already has review, grab primary key for update
        try:
            user_review = Reviews.objects.get(user=request.user.id, joint=joint_id)
            user_pk = user_review.id
            user_created = user_review.created
        except:
            user_pk = None
            user_created = datetime.datetime.now()
    except Joints.DoesNotExist:
        raise Http404
    else:   
        Reviews(pk=user_pk, joint_id=joint_id, user_id=request.user.id, rating=p['rating'], review=p['review'], created = user_created, updated = datetime.datetime.now()).save()
        # Reviews(pk=user_pk, joint_id=joint_id, user_id=request.user.id, rating=p['rating'], review=p['review']).save()
        context = RequestContext(request)
        return render_to_response('joint.html', {'joint': j, 'state': s, 'request': p}, context_instance=RequestContext(request))
