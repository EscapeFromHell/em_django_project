from django.db import models
from registration.models import Company, User


class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_department",
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    company = models.ForeignKey(
        Company, related_name="departments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class Position(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, related_name="positions", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees"
    )
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="employees"
    )
    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
