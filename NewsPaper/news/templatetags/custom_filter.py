from django import template
from django.contrib.auth.models import User


register = template.Library()


@register.filter(name='censor')
def censor(value):
    words = value.split()
    result = []
    forbidden_words = ['radish', 'fool', 'boob', 'moron', 'asshole', 'assholes']
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

