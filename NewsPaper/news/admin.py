from django.contrib import admin
from .models import Category, Post, Comment, Author, PostCategory, Subscribers


class PostAdmin(admin.ModelAdmin):
    # list_display is a list or tuple with all the fields you want to see in the product table
    list_display = ('title', 'categoryType', 'rating')
    list_filter = ('rating', 'dateCreation')  # add primitive filters to our admin panel
    search_fields = ('title', 'categoryType')  # everything here is very similar to filters from queries to the database


class AuthorAdmin(admin.ModelAdmin):
    # list_display — this is a list or tuple with all the fields that you want to see in the product table
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = (['ratingAuthor'])  # adding primitive filters to our admin panel
    search_fields = ('authorUser', 'ratingAuthor')  # everything here is very similar to filters from queries to the database


class SubscribersAdmin(admin.ModelAdmin):
    # list_display — this is a list or tuple with all the fields that you want to see in the product table
    list_display = ('subscriber', 'category')
    list_filter = (['category'])  # adding primitive filters to our admin panel
    search_fields = (['subscriber'])  # everything here is very similar to filters from queries to the database


class CategoryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory)
admin.site.register(Subscribers, SubscribersAdmin)
