from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать, создавать, редактировать и удалять задачи.

    Этот ViewSet предоставляет следующие действия:
    - list: Получение списка всех задач.
    - create: Создание новой задачи.
    - retrieve: Получение конкретной задачи по ID.
    - update: Обновление задачи по ID.
    - partial_update: Частичное обновление задачи по ID.
    - destroy: Удаление задачи по ID.

    Каждая задача содержит следующую информацию:
    - title: Заголовок задачи.
    - description: Подробное описание задачи.
    - author: Пользователь, который создал задачу.
    - assignee: Пользователь, ответственный за выполнение задачи.
    - observers: Список пользователей, наблюдающих за задачей.
    - executors: Список пользователей, выполняющих задачу.
    - deadline: Срок выполнения задачи.
    - status: Текущий статус задачи (Новое, В процессе, Завершено).
    - estimated_time: Оценочное время для выполнения задачи.

    Права доступа:
    - Только аутентифицированные пользователи могут получить доступ к этому ViewSet.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
