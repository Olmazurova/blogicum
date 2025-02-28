# users/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Получаем модель пользователя:
User = get_user_model()


class UserBlogicumCreationForm(UserCreationForm):
    """
    Изменённый класс формы регистрации.
    """

    # Наследуем класс Meta от соответствующего класса родительской формы.
    # Так этот класс будет не перезаписан, а расширен.
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
