from django.contrib import admin
from .models import Enrollment, Course, Lesson, LessonBooking
from django.utils.safestring import mark_safe
from django import forms

# Define the form for Enrollment
class EnrollmentFormAdmin(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['user', 'course', 'enrollment_type']  # Fields to display in the form

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    form = EnrollmentFormAdmin  # Link the custom form to the admin panel
    list_display = ('user', 'username', 'course', 'enrollment_type', 'enrollment_date')
    search_fields = ('user__username', 'user__email', 'course__title', 'username')
    list_filter = ('course', 'enrollment_type')

    def username(self, obj):
        return obj.user.username  # Access username via the 'user' field
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email  # Access email via the 'user' field
    email.short_description = 'Email'

    def level(self, obj):
        return obj.user.level  # Assuming the 'user' model has a 'level' field
    level.short_description = 'Level'

# Continue with the rest of your admin registrations...
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course_type', 'lessons_count', 'price_in_yen', 'display_image')
    search_fields = ('title',)
    fields = ('title', 'description', 'course_type', 'lessons_count', 'price_in_yen', 'image', 'materials')

    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No image available"
    display_image.short_description = 'Image'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'start_time', 'materials', 'zoom_link')
    search_fields = ('title', 'course__title', 'teacher__username')
    fields = ('course', 'title', 'teacher', 'start_time', 'content', 'duration', 'video_url', 'zoom_link', 'materials')

@admin.register(LessonBooking)
class LessonBookingAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'lesson_type', 'schedule')
    search_fields = ['lesson__title', 'user__username']
    list_filter = ('lesson_type',)
