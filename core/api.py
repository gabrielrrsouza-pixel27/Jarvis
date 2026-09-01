import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from core.services.orchestrator import JarvisOrchestrator


@csrf_protect
def chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required.'}, status=405)
    try:
        payload = json.loads(request.body or '{}')
        result = JarvisOrchestrator().respond(
            text=payload.get('message', ''),
            tool_name=payload.get('tool'),
            tool_parameters=payload.get('parameters'),
            confirmed=payload.get('confirmed', False),
        )
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    except PermissionError as exc:
        return JsonResponse({'error': str(exc)}, status=403)
    return JsonResponse(result)
