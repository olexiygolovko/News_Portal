from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscriber = models.ManyToManyField(User, through='Subscribers')

    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title.title()}'


    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the parent method to save the object


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryThrough} | {self.postThrough}'


    class Meta:
        verbose_name = 'News category'
        verbose_name_plural = 'News categories'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def __str__(self):
        return f'{self.text}'


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Subscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subscriber}  {self.category}'


    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
