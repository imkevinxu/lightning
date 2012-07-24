from lightning_app.models import *
from django.contrib import admin

from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mass_mail

bodyTemplate = get_template('email.txt')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'location', 'fhp_id', 'is_invited')
    list_filter = ('is_invited', 'created_at')
    ordering = ['-created_at']
    search_fields = ['fullname']
    actions = ['invite']

    # TODO: send email with unique registration code when invited by admin
    def invite(self, request, queryset):
        subject = "You've been invited to Lightning"

        queryset.update(is_invited=True)

        messages = []
        for user in queryset:
            context = Context({
                'username': user.user.username
            })
            
            body = bodyTemplate.render(context)

            if len(user.user.email) > 0:
                messages.append((subject, body, 'me@wylie.su', [user.user.email]))

        print messages

        send_mass_mail(messages)

    invite.short_description = "Invite user"

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