import re

from core.models import Memory


STOP_WORDS = {
    'a', 'as', 'ao', 'aos', 'com', 'como', 'da', 'das', 'de', 'do', 'dos',
    'e', 'em', 'essa', 'esse', 'esta', 'este', 'eu', 'for', 'na', 'nas',
    'no', 'nos', 'o', 'os', 'para', 'por', 'que', 'se', 'sobre', 'um',
    'uma', 'voce', 'you', 'the', 'what', 'should', 'use', 'i', 'is', 'my',
}


def _keywords(value: str) -> set[str]:
    return {
        word.lower()
        for word in re.findall(r'[A-Za-zÀ-ÿ0-9]+', value)
        if len(word) > 2 and word.lower() not in STOP_WORDS
    }


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

    def relevant_context(self, query: str, limit: int = 5) -> list[Memory]:
        if limit < 1:
            raise ValueError('Memory context limit must be positive.')
        query_keywords = _keywords(query)
        memories = list(Memory.objects.all())
        ranked = []
        for memory in memories:
            overlap = query_keywords & _keywords(memory.content)
            if overlap:
                score = (len(overlap), memory.importance, memory.updated_at)
                ranked.append((score, memory))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [memory for _, memory in ranked[:limit]]

    def forget(self, memory_id: int) -> None:
        deleted, _ = Memory.objects.filter(id=memory_id).delete()
        if not deleted:
            raise ValueError('Memory not found.')
