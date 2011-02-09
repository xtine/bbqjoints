from joints.models import Joints, States
from django.shortcuts import render_to_response

def index(request):
    list_of_states = States.objects.all().order_by('state_abbr')
    return render_to_response('joints.html', {'list_of_states': list_of_states})
    
def state(request, state_abbr):
    try:
        # s = Joints.objects.get(state__state_abbr=state_abbr)
        s = Joints.objects.filter(state__state_abbr=state_abbr)
    except Joints.DoesNotExist:
        raise Http404
    return render_to_response('state.html', {'state': s})
    
def joint(request, joint_id):
    try:
        j = Joints.objects.get(pk=joint_id)
    except Joints.DoesNotExist:
        raise Http404
    return render_to_response('joint.html', {'joint': j})