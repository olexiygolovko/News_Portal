from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

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

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]