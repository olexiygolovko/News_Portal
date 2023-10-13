from .models import Category, Post, PostCategory
from modeltranslation.translator import register, TranslationOptions



@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text')  # indicate which fields should be translated as a tuple


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


