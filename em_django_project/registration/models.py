from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class User(AbstractUser):
    first_name = models.CharField(
        "Имя",
        max_length=150,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
    )
    account = models.EmailField(
        "Почта",
        max_length=254,
        unique=True,
    )
    company = models.ForeignKey(
        Company,
        related_name="employees",
        on_delete=models.CASCADE,
    )
    is_staff = models.BooleanField("Администратор", default=False)
    is_active = models.BooleanField("Активация", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(
        max_length=150, unique=False, blank=True, null=True, default=None
    )

    EMAIL_FIELD = "account"
    USERNAME_FIELD = "account"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class AccountInvite(models.Model):
    account = models.EmailField("Почта", max_length=254, unique=True)
    invite_token = models.CharField("Токен", max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account

    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"
