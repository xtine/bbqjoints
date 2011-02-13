from joints.models import Joints, States
from django.shortcuts import render_to_response

from django.template import RequestContext


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
    context = RequestContext(request)
    return render_to_response('joint.html', {'joint': j, 'state': s}, context_instance=context)