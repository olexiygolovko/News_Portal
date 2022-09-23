from .models import Category, Post, PostCategory
from modeltranslation.translator import register, TranslationOptions



@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text')  # указываем, какие именно поля надо переводить в виде кортежа


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


