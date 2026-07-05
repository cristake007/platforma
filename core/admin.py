from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_avatar')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    @admin.display(boolean=True, description='Avatar')
    def has_avatar(self, profile):
        return bool(profile.avatar)
