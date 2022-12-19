from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import CustomUser, UserProfile

# Register your models here
'''

class CustomUserAdmin(UserAdmin):
    #add_form = CustomUserCreationForm
    #form = CustomUserChangeForm

    model = CustomUser

    list_display = ('email',
                    'phone_number',
                    'role', 
                    'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 
                           'email',
                           'role', 
                           'password')}),
        ('Permissions', {'fields': ('is_staff', 
                                    'is_active',
                                    'is_superuser', 
                                    'groups', 
                                    'user_permissions')}),
        ('Dates', {'fields': ('last_login', 
                              'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 
                       'email',
                       'groups',  
                       'password1', 
                       'password2',
                        'role', 
                       )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
'''
#admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUser)
admin.site.register(UserProfile)
