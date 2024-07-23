from django.contrib import admin
from .models import UserProfile, RelationshipStatus, Comment


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'date_of_birth', 'zodiac')
    search_fields = ('user__username', 'location', 'zodiac')
    list_filter = ('zodiac',)


class RelationshipStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'color')
    search_fields = ('user__username', 'status')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'text')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RelationshipStatus, RelationshipStatusAdmin)
admin.site.register(Comment, CommentAdmin)
