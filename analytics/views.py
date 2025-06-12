from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import PageView, Conversion
import json
from django.shortcuts import render

@csrf_exempt
def track_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event_type = data.get('event_type')
        session_id = data.get('session_id')
        
        if event_type == 'page_view':
            PageView.objects.create(
                session_id=session_id,
                page_url=data.get('page_url', ''),
                user_agent=data.get('user_agent', ''),
                ip_address=request.META.get('REMOTE_ADDR')
            )
        elif event_type == 'conversion':
            Conversion.objects.create(
                session_id=session_id,
                conversion_type=data.get('conversion_type', ''),
                value=data.get('value', None)
            )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error' }, status=400)

def dashboard(request):
    return(render(request, "analystics/dashboard.html"))