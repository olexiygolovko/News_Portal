from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Post, Category, PostCategory, Subscribers

class NewsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['author'].label = "Author's name"
        self.fields['categoryType'].label = 'Publication type'
        self.fields['postCategory'].label = 'Categories'
        self.fields['title'].label = 'Heading'
        self.fields['text'].label = 'Text'


    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'postCategory', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "The description should not be identical to the title."
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


class SubscribeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.get('prefix')
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(subscriber=user.id)

    class Meta:
        model = Subscribers
        fields = [
            'category',
        ]
