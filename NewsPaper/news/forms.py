from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class NewsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['author'].label = 'Имя автора'
        self.fields['categoryType'].label = 'Вид публикации'
        self.fields['postCategory'].label = 'Категории'
        self.fields['title'].label = 'Заголовок'
        self.fields['text'].label = 'Текст'


    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'postCategory', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
