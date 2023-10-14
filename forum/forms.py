from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import ForumUser, Answers, Questions

SUBJECT_CHOICE = (
    ('chemistry', 'Химия'),
    ('biology', 'Биология'),
    ('physics', 'Физика'),
    ('math', 'Математика'),
    ('it', 'Информатика'),
    ('english', 'Английский'),
    ('russian', 'Русский')
)

class RegForm(forms.ModelForm):
    grade = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Класс не может быть меньше 1"),
            MaxValueValidator(11, message="Класс не может быть больше 11")
        ]
    )
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages = {
            'unique': "Эта почта уже зарегистрирована",
        }
        self.fields['username'].error_messages = {
            'unique': "Это имя пользователя уже занято"
        }

    class Meta:
        model = ForumUser
        fields = ['grade', 'username', 'email', 'first_name', 'last_name', 'password']

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangeProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Фото профиля')
    username = forms.CharField(label='Имя пользователя')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.CharField(required=False, widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = ForumUser
        fields = ['profile_image', 'first_name', 'last_name', 'username', 'password', 'email']

class QuestionForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    subject = forms.ChoiceField(widget=forms.RadioSelect, choices=SUBJECT_CHOICE)

    class Meta:
        model = Questions
        fields = ['image', 'subject', 'title', 'content']

class AnswerForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Answers
        fields = ['image', 'content']