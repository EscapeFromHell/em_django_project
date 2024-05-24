from django.contrib import admin
from organization_structure.models import Department, Employee, Position


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "company")
    search_fields = (
        "name",
        "manager__first_name",
        "manager__last_name",
        "company__name",
    )
    list_filter = ("company",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "position", "manager")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "department__name",
        "position__name",
    )
    list_filter = ("department", "position")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "department")
    search_fields = ("name",)
    list_filter = ("department",)
