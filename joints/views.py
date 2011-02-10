from joints.models import Joints, States
from django.shortcuts import render_to_response

def index(request):
    list_of_states = States.objects.all().order_by('name')
    return render_to_response('states_listing.html', {'list_of_states': list_of_states})
    
def state(request, state_abbr):
    try:
        j = Joints.objects.filter(state__state_abbr=state_abbr)
        s = States.objects.get(state_abbr=state_abbr)
    except Joints.DoesNotExist:
        raise Http404
    return render_to_response('state.html', {'joints': j, 'state': s})
    
def joint(request, joint_id):
    try:
        j = Joints.objects.get(pk=joint_id)
        s = States.objects.get(state_abbr=j.state)
    except Joints.DoesNotExist:
        raise Http404
    return render_to_response('joint.html', {'joint': j, 'state': s})