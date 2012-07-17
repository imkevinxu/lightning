from lightning_app.models import *
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'fhp_id', 'created_at')
    list_filter = ('created_at',)
    ordering = ['-created_at']
    search_fields = ['fullname']

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_id', 'user', 'rating', 'times_viewed', 'votes_count', 'favorites_count', 'comments_count')
    list_filter = ('created_at',)
    ordering = ['-created_at']
    search_fields = ['name', 'photo_id']

class TagAdmin(admin.ModelAdmin):
    list_display = ('tagname',)
    search_fields = ['tagname']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tag, TagAdmin)