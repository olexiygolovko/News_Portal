from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    words = value.split()
    result = []
    forbidden_words = ['редиска', 'дурак', 'балбес', 'придурок', 'мудак', 'мудаки']
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
