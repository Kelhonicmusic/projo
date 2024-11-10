from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import CustomUser, Enrollment
from .models import Booking
from .models import LessonBooking
from .models import Enrollment, CustomUser



class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    interests = forms.CharField(widget=forms.Textarea)
    hobbies = forms.CharField(widget=forms.Textarea)
    countries_travelled = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'full_name', 'email', 'phone_number', 'gender', 
            'level', 'interests', 'hobbies', 'countries_travelled', 
            'password1', 'password2'
        ]


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)



class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['enrollment_type']



class LessonBookingForm(forms.ModelForm):
    class Meta:
        model = LessonBooking
        fields = ['user', 'lesson', 'lesson_type', 'schedule']