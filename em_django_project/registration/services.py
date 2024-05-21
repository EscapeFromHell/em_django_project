import random
import string

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import AccountInvite, Company, User
from .serializers import AccountInviteSerializer, UserSerializer


def check_account(query_params: QueryDict) -> tuple:
    """
    Проверяет, существует ли аккаунт.

    Аргументы:
    - query_params: параметры запроса.

    Возвращает:
    - (False, str), если аккаунт существует или указан не валидный email.
    - (True, None), если аккаунт с таким email не существует.
    """
    account = query_params.get("account")
    try:
        validate_email(account)
    except ValidationError:
        return False, "Invalid email address"

    try:
        AccountInvite.objects.get(account=account)
        return False, "Account with this email already exist"
    except AccountInvite.DoesNotExist:
        return True, None


def create_invite_token(query_params: QueryDict) -> str | None:
    """
    Создает токен приглашения для регистрации.

    Аргументы:
    - query_params: параметры запроса.

    Возвращает:
    - Строку с токеном приглашения.
    """
    account = query_params.get("account")
    invite_token = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    account_invite_serializer = AccountInviteSerializer(
        data={"account": account, "invite_token": invite_token}
    )
    if account_invite_serializer.is_valid():
        account_invite_serializer.save()
        return invite_token


def send_invite_email(params: dict, invite_token: str | None = None) -> None:
    """
    Отправляет электронное письмо с приглашением для регистрации.

    Аргументы:
    - params: параметры запроса.
    - invite_token: токен приглашения (необязательно).

    Возвращает:
    - None.
    """
    account = params.get("account")
    subject = "Подтверждение регистрации"
    if invite_token:
        message = (
            f"Для завершения регистрации введите код подтверждения: {invite_token}"
        )
    else:
        message = (
            "Для завершения регистрации перейдите по ссылке и введите пароль: "
            f"http://127.0.0.1:8000/auth/api/v1/confirm-registration/?account={account}"
        )
    from_email = "email@example.com"
    recipient_list = [account]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Произошла ошибка при отправке письма: {e}")

    print(
        f"Тема: {subject}, Сообщение: {message}, От: {from_email}, Кому: {recipient_list}"
    )


def confirm_account(request_data: dict) -> bool:
    """
    Подтверждает учетную запись пользователя.

    Аргументы:
    - request_data: данные запроса.

    Возвращает:
    - True, если учетная запись подтверждена.
    - False, если учетная запись или токен недействительны.
    """
    account = request_data.get("account")
    invite_token = request_data.get("invite_token")
    try:
        AccountInvite.objects.get(account=account, invite_token=invite_token)
        return True
    except AccountInvite.DoesNotExist:
        return False


def create_company(company_name: str) -> tuple:
    """
    Создает компанию.

    Аргументы:
    - company_name: имя компании.

    Возвращает:
    - Объект компании или None, если компания уже существует.
    """
    company, is_created = Company.objects.get_or_create(company_name=company_name)
    if is_created:
        print("Company created")
        return company, is_created
    else:
        print("Company already exists")
        return None, is_created


def create_admin_user(request_data: dict) -> tuple:
    """
    Создает компанию и администратора компании.

    Аргументы:
    - request_data: данные запроса.

    Возвращает:
    - Кортеж с данными о созданном администраторе, компании и статусом HTTP.
    """
    company_name = request_data.get("company_name")
    if not company_name:
        return "Company name is required", status.HTTP_400_BAD_REQUEST
    company, is_created = create_company(company_name)
    if not is_created:
        return "Company already exists", status.HTTP_400_BAD_REQUEST
    request_data["company"] = company.pk
    print(company.pk)
    request_data["is_staff"] = request_data["is_active"] = True
    print(request_data)
    serializer_user = UserSerializer(data=request_data)
    if serializer_user.is_valid():
        user = serializer_user.save()
        user_serializer = UserSerializer(user).data
        return user_serializer, status.HTTP_201_CREATED
    else:
        return serializer_user.errors, status.HTTP_400_BAD_REQUEST


def create_user(request_data: dict, user: User) -> tuple:
    """
    Создает нового пользователя.

    Аргументы:
    - request_data: данные запроса.
    - user: объект текущего пользователя.

    Возвращает:
    - Кортеж с данными о созданном пользователе и статусом HTTP.
    """
    request_data["company"] = user.company.pk
    request_data["is_active"] = False
    request_data["is_staff"] = request_data.get("is_staff", False)
    serializer_user = UserSerializer(data=request_data)
    if serializer_user.is_valid():
        serializer_user.save()
        send_invite_email(params=request_data)
        return serializer_user.data, status.HTTP_201_CREATED
    else:
        return serializer_user.errors, status.HTTP_400_BAD_REQUEST


def activate_user(request_data: dict, query_params: QueryDict) -> tuple:
    """
    Активирует пользователя.

    Аргументы:
    - request_data: данные запроса.
    - query_params: параметры запроса.

    Возвращает:
    - Кортеж с данными о пользователе и статусом HTTP или сообщением об ошибке.
    """
    user = get_object_or_404(User, account=query_params.get("account"))
    entered_password = request_data.get("password")
    is_correct_password = check_password(entered_password, user.password)
    if is_correct_password:
        user.is_active = True
        user.save()
        user_serializer = UserSerializer(user).data
        return user_serializer, status.HTTP_200_OK
    else:
        return "Password is incorrect", status.HTTP_403_FORBIDDEN


def update_user(request_data: dict, user: User) -> tuple:
    """
    Обновляет информацию о пользователе.

    Аргументы:
    - request_data: данные запроса.
    - user: объект текущего пользователя.

    Возвращает:
    - Кортеж с данными об обновленном пользователе и статусом HTTP или сообщением об ошибке.
    """
    allowed_keys = {"first_name", "last_name", "account"}
    if not set(request_data.keys()).issubset(allowed_keys):
        return (
            "Only first_name, last_name and account can be updated",
            status.HTTP_400_BAD_REQUEST,
        )
    serializer_user = UserSerializer(user, data=request_data, partial=True)
    if serializer_user.is_valid():
        user = serializer_user.save()
        user_serializer = UserSerializer(user).data
        return user_serializer, status.HTTP_201_CREATED
    else:
        return serializer_user.errors, status.HTTP_400_BAD_REQUEST
