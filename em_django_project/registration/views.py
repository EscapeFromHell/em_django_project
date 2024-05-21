from django.http import HttpResponseRedirect
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from . import services


class RegistrationViewSet(viewsets.ViewSet):
    """
    Представление для регистрации пользователей.

    Методы:
    - check_account: проверка существования аккаунта.
    - sign_up: регистрация нового пользователя.
    - sign_up_complete: завершение регистрации и создание компании и администратора.
    - create_user: создание нового пользователя.
    - confirm_registration: подтверждение регистрации.
    - update_user: обновление информации о пользователе.
    """

    @action(url_path="check_account", detail=False, methods=["get"])
    def check_account(self, request: Request) -> HttpResponseRedirect | Response:
        """
        Проверяет существование аккаунта.

        Аргументы:
        - request: объект запроса.

        Возвращает:
        - HttpResponseRedirect на страницу регистрации, если аккаунт не существует.
        - Response с сообщением об ошибке, если аккаунт уже существует или указан невалидный email.
        """
        account_check, message = services.check_account(
            query_params=request.query_params
        )
        if account_check:
            invite_token = services.create_invite_token(
                query_params=request.query_params
            )
            services.send_invite_email(
                params=request.query_params, invite_token=invite_token
            )
            return HttpResponseRedirect("/auth/api/v1/sign-up/")
        else:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path="sign-up", detail=False, methods=["post"])
    def sign_up(self, request: Request) -> HttpResponseRedirect | Response:
        """
        Регистрирует нового пользователя.

        Аргументы:
        - request: объект запроса.

        Возвращает:
        - HttpResponseRedirect на страницу завершения регистрации, если регистрация успешна.
        - Response с сообщением об ошибке, если данные неверны.
        """
        is_valid = services.confirm_account(request_data=request.data)
        if is_valid:
            return HttpResponseRedirect("/auth/api/v1/sign-up-complete/")
        else:
            return Response(
                data="Account or token is invalid", status=status.HTTP_400_BAD_REQUEST
            )

    @action(url_path="sign-up-complete", detail=False, methods=["post"])
    def create_company_and_admin(self, request: Request) -> Response:
        """
        Завершает регистрацию, создавая компанию и администратора.

        Аргументы:
        - request: объект запроса.

        Возвращает:
        - Response с данными о созданной компании и администраторе или сообщением об ошибке.
        """
        response, status_code = services.create_admin_user(request_data=request.data)
        return Response(data=response, status=status_code)

    @action(
        url_path="create_user",
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsAdminUser],
    )
    def create_new_user(self, request: Request) -> Response:
        """
        Создает нового пользователя.

        Аргументы:
        - request: объект запроса.

        Возвращает:
        - Response с данными о созданном пользователе или сообщением об ошибке.
        """
        response, status_code = services.create_user(
            request_data=request.data, user=request.user
        )
        return Response(data=response, status=status_code)

    @action(url_path="confirm-registration", detail=False, methods=["patch"])
    def confirm_registration(self, request: Request) -> Response:
        """
        Подтверждает регистрацию пользователя.

        Аргументы:
        - request: объект запроса.

        Возвращает:
        - Response с данными о подтвержденном пользователе или сообщением об ошибке.
        """
        response, status_code = services.activate_user(
            request_data=request.data, query_params=request.query_params
        )
        return Response(data=response, status=status_code)

    @action(
        url_path="update_user",
        detail=False,
        methods=["put"],
        permission_classes=[IsAuthenticated],
    )
    def update_employee(self, request: Request) -> Response:
        """
        Обновляет информацию о пользователе.

        Аргументы:
        - request: объект запроса.

        Возвращает:
        - Response с данными об обновленном пользователе или сообщением об ошибке.
        """
        response, status_code = services.update_user(request.data, request.user)
        return Response(data=response, status=status_code)
