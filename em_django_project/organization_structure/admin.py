from django.contrib import admin

from organization_structure.models import Department, Employee, Position

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Position)
