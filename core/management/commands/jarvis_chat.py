from django.core.management.base import BaseCommand

from core.models import Conversation
from core.services.orchestrator import JarvisOrchestrator


class Command(BaseCommand):
    help = 'Start an interactive JARVIS terminal conversation.'

    def handle(self, *args, **options):
        orchestrator = JarvisOrchestrator()
        conversation = None
        self.stdout.write(self.style.SUCCESS('JARVIS terminal ready. Type :quit to exit.'))

        while True:
            try:
                text = input('You: ').strip()
            except (EOFError, KeyboardInterrupt):
                self.stdout.write('\nJARVIS: Session ended.')
                break

            if text.lower() in {':quit', ':exit'}:
                self.stdout.write('JARVIS: Session ended.')
                break
            if not text:
                continue

            try:
                result = orchestrator.respond(text, conversation=conversation)
                conversation = Conversation.objects.get(id=result['conversation_id'])
                self.stdout.write(f"JARVIS: {result['answer']}")
            except (ValueError, PermissionError, RuntimeError) as exc:
                self.stderr.write(f'JARVIS error: {exc}')
