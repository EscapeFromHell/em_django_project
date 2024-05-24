from django.contrib import admin
from registration.models import AccountInvite, Company, User


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name",)
    search_fields = ("company_name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "account",
        "company",
        "is_staff",
        "is_active",
    )
    search_fields = ("first_name", "last_name", "account")
    list_filter = ("is_staff", "company")


@admin.register(AccountInvite)
class AccountInviteAdmin(admin.ModelAdmin):
    list_display = ("account", "invite_token")
    search_fields = ("account",)
