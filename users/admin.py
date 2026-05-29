from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'is_staff')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Медицинские & E-commerce данные клиники', {
            'fields': ('phone', 'address'),
        }),
    )

# Ленивая чистая регистрация
UserClass = get_user_model()
try:
    admin.site.unregister(UserClass)
except admin.sites.NotRegistered:
    pass

admin.site.register(UserClass, UserAdmin)
