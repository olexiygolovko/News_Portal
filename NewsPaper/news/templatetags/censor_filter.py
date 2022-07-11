from django import template


register = template.Library()

@register.filter(name='censor')
def censor(text):
    badwords = ('редиска', 'дурак', 'балбес', 'придурок', 'мудак', 'мудаки')
    sentence = text.split()

    for index, word in enumerate(sentence):
        if any(badword in word.lower() for badword in badwords):
            sentence[index] = "".join('*' if c.isalpha() else c for c in word)

    return " ".join(sentence)