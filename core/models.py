from django.db import models


class Conversation(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
	class Role(models.TextChoices):
		USER = 'user', 'User'
		ASSISTANT = 'assistant', 'Assistant'
		TOOL = 'tool', 'Tool'

	conversation = models.ForeignKey(
		Conversation,
		on_delete=models.CASCADE,
		related_name='messages',
	)
	role = models.CharField(max_length=20, choices=Role.choices)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)


class Memory(models.Model):
	content = models.TextField()
	category = models.CharField(max_length=50, default='fact')
	importance = models.PositiveSmallIntegerField(default=5)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class ToolAuditLog(models.Model):
	tool_name = models.CharField(max_length=100)
	parameters = models.JSONField(default=dict)
	result = models.JSONField(default=dict)
	risk_level = models.CharField(max_length=20)
	confirmed_by_user = models.BooleanField(default=False)
	success = models.BooleanField(default=False)
	duration_ms = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
