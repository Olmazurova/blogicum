from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Форма отдельного поста на основе модели поста."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }
