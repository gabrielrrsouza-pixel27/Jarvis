import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from core.services.memory import MemoryService
from core.models import Conversation
from core.services.orchestrator import JarvisOrchestrator


@csrf_protect
def chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required.'}, status=405)
    try:
        payload = json.loads(request.body or '{}')
        tool_call = payload.get('tool_call') or {}
        conversation = None
        if payload.get('conversation_id') is not None:
            conversation = Conversation.objects.get(id=payload['conversation_id'])
        result = JarvisOrchestrator().respond(
            text=payload.get('message', ''),
            conversation=conversation,
            tool_name=payload.get('tool') or tool_call.get('name'),
            tool_parameters=payload.get('parameters') or tool_call.get('arguments'),
            confirmed=payload.get('confirmed', False),
        )
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found.'}, status=404)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    except PermissionError as exc:
        return JsonResponse({'error': str(exc)}, status=403)
    except RuntimeError as exc:
        return JsonResponse({'error': str(exc)}, status=502)
    return JsonResponse(result)


def _memory_payload(memory):
    return {
        'id': memory.id,
        'content': memory.content,
        'category': memory.category,
        'importance': memory.importance,
        'created_at': memory.created_at.isoformat(),
        'updated_at': memory.updated_at.isoformat(),
    }


@csrf_protect
def memories(request):
    service = MemoryService()
    if request.method == 'GET':
        items = service.search(request.GET.get('q', ''))
        return JsonResponse({'memories': [_memory_payload(item) for item in items]})
    if request.method == 'POST':
        try:
            payload = json.loads(request.body or '{}')
            memory = service.save(
                content=payload.get('content', ''),
                category=payload.get('category', 'fact'),
                importance=payload.get('importance', 5),
            )
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            return JsonResponse({'error': str(exc)}, status=400)
        return JsonResponse(_memory_payload(memory), status=201)
    return JsonResponse({'error': 'GET or POST required.'}, status=405)


@csrf_protect
def forget_memory(request, memory_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'DELETE required.'}, status=405)
    try:
        MemoryService().forget(memory_id)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=404)
    return JsonResponse({'deleted': memory_id})
