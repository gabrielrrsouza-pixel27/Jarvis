from core.models import Memory


class MemoryService:
    def save(self, content: str, category: str = 'fact', importance: int = 5) -> Memory:
        content = content.strip()
        if not content:
            raise ValueError('Memory content cannot be empty.')
        if not 1 <= importance <= 10:
            raise ValueError('Importance must be between 1 and 10.')
        return Memory.objects.create(
            content=content,
            category=category.strip() or 'fact',
            importance=importance,
        )

    def search(self, query: str = '') -> list[Memory]:
        memories = Memory.objects.all().order_by('-importance', '-updated_at')
        query = query.strip()
        if query:
            memories = memories.filter(content__icontains=query)
        return list(memories)

    def forget(self, memory_id: int) -> None:
        deleted, _ = Memory.objects.filter(id=memory_id).delete()
        if not deleted:
            raise ValueError('Memory not found.')
