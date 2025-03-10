from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма отдельного поста на основе модели поста."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    """Форма комментирования отдельного поста на основе модели коммента."""

    class Meta:
        model = Comment
        fields = ('text',)
