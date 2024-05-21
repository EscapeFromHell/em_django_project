from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import AccountInvite, Company, User


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            "pk",
            "company_name",
        )


class UserSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    company_details = CompanySerializer(source="company", read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "password",
            "account",
            "company",
            "company_details",
            "is_staff",
            "is_active",
        )

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def create(self, validated_data):
        company = validated_data.pop("company")
        validated_data["username"] = " "
        user = User.objects.create_user(**validated_data, company=company)
        return user


class AccountInviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountInvite
        fields = (
            "account",
            "invite_token",
        )
