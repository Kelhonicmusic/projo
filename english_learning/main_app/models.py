from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Custom User model with roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    # Fields
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=6, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True,
        null=True
    )
    level = models.CharField(max_length=50, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    countries_travelled = models.TextField(blank=True, null=True)
    lessons = models.ManyToManyField('Lesson', related_name='teachers', blank=True)  # Use string notation here
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        blank=False,
        null=False,
    )

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    def __str__(self):
        return self.username


# Course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_type = models.CharField(max_length=100)
    lessons_count = models.PositiveIntegerField()
    price_in_yen = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    materials = models.FileField(upload_to='course_materials/', blank=True, null=True)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses') 

    def __str__(self):
        return self.title

# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(null=True, blank=True)
    zoom_link = models.URLField(blank=True, null=True)
    materials = models.FileField(upload_to='lesson_materials/', blank=True, null=True)
    completed = models.BooleanField(default=False) 
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'}  # Restricts to users with 'teacher' role
    )

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    ENROLLMENT_TYPES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_type = models.CharField(max_length=10, choices=ENROLLMENT_TYPES, default='free')
    enrollment_date = models.DateTimeField(default=timezone.now)
  
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        default=1 
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')],
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {self.status}"

class LessonBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, default=1)  # Assuming course with ID 1 exists
    lesson_type = models.CharField(
        max_length=50, 
        choices=[('private', 'Private'), ('semi_private', 'Semi Private'), ('group', 'Group')]
    )
    schedule = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=[('booked', 'Booked'), ('completed', 'Completed')],
        default='booked'  # Set a default value
    )

    def __str__(self):
        return f"{self.lesson_type} booking for {self.user.username} on {self.schedule}"



