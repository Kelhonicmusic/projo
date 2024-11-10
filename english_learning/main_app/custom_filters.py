from django import template

register = template.Library()

@register.filter
def is_enrolled(course, user):
    return course.enrolled_users.filter(id=user.id).exists()