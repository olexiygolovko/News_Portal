from django.contrib import admin
from .models import Category, Post, Comment, Author, PostCategory, Subscribers


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'categoryType', 'rating')
    list_filter = ('rating', 'dateCreation')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'categoryType')  # тут всё очень похоже на фильтры из запросов в базу


class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = (['ratingAuthor'])  # добавляем примитивные фильтры в нашу админку
    search_fields = ('authorUser', 'ratingAuthor')  # тут всё очень похоже на фильтры из запросов в базу


class SubscribersAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('subscriber', 'category')
    list_filter = (['category'])  # добавляем примитивные фильтры в нашу админку
    search_fields = (['subscriber'])  # тут всё очень похоже на фильтры из запросов в базу


class CategoryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory)
admin.site.register(Subscribers, SubscribersAdmin)
