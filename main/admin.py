from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Appointment, MentorProfile, MenteeProfile, MentorTags, MenteeTags, MentorMenteeScore


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name','last_name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'email_confirmed','admin_approved', 'is_admin', 'is_mentor', 'is_mentee')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ('datetime', 'mentor','mentee','accepted_by_mentor',)

admin.site.register(Appointment,AppointmentAdmin)

class MentorProfileAdmin(admin.ModelAdmin):
    model = MentorProfile
    list_display = ('user', 'mentor_first_name', 'mentor_last_name', 'mentor_email','field_of_design','place_of_work','url','bio', )

admin.site.register(MentorProfile,MentorProfileAdmin)

class MenteeProfileAdmin(admin.ModelAdmin):
    model = MenteeProfile
    list_display = ('user', 'mentee_first_name', 'mentee_last_name', 'mentee_email','field_of_design','place_of_work','url','bio', )

admin.site.register(MenteeProfile,MenteeProfileAdmin)

class MentorTagsAdmin(admin.ModelAdmin):
    model = MentorTags
    list_display = ('id','tag', 'tag_auto_bio','match_id',)

admin.site.register(MentorTags,MentorTagsAdmin)

class MenteeTagsAdmin(admin.ModelAdmin):
    model = MenteeTags
    list_display = ('id','tag', 'match_id',)

admin.site.register(MenteeTags,MenteeTagsAdmin)

class MentorMenteeScoreAdmin(admin.ModelAdmin):
    model = MentorMenteeScore
    list_display = ('score', 'mentor', 'mentee',)

admin.site.register(MentorMenteeScore,MentorMenteeScoreAdmin)