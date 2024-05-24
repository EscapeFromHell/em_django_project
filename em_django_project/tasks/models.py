from django.db import models
from registration.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(
        User, related_name="authored_tasks", on_delete=models.SET_NULL, null=True
    )
    assignee = models.ForeignKey(
        User, related_name="assigned_tasks", on_delete=models.SET_NULL, null=True
    )
    observers = models.ManyToManyField(User, related_name="observed_tasks")
    executors = models.ManyToManyField(User, related_name="executed_tasks")
    deadline = models.DateTimeField()
    STATUS_CHOICES = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    estimated_time = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
