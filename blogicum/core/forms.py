from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


User = get_user_model()

class UserEditForm(UserChangeForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)