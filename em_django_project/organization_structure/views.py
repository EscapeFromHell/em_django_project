from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Department, Employee, Position
from .serializers import DepartmentSerializer, EmployeeSerializer, PositionSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint, позволяющий просматривать, создавать, редактировать и удалять подразделения компании.

    Доступные действия:
    - list: Получение списка всех подразделений.
    - create: Создание нового подразделения.
    - retrieve: Получение конкретного подразделения по ID.
    - update: Обновление подразделения по ID.
    - partial_update: Частичное обновление подразделения по ID.
    - destroy: Удаление подразделения по ID.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint, позволяющий просматривать, создавать, редактировать и удалять должности в компании.

    Доступные действия:
    - list: Получение списка всех должностей.
    - create: Создание новой должности.
    - retrieve: Получение конкретной должности по ID.
    - update: Обновление должности по ID.
    - partial_update: Частичное обновление должности по ID.
    - destroy: Удаление должности по ID.
    """

    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint, позволяющий просматривать, создавать, редактировать и удалять сотрудников в компании.

    Доступные действия:
    - list: Получение списка всех сотрудников.
    - create: Создание нового сотрудника.
    - retrieve: Получение конкретного сотрудника по ID.
    - update: Обновление данных сотрудника по ID.
    - partial_update: Частичное обновление данных сотрудника по ID.
    - destroy: Удаление сотрудника по ID.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
