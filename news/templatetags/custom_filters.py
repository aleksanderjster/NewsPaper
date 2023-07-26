from django import template
from .censor_words import ILLEGAL_WORDS
import re

register = template.Library()

# register our filter for templates.
@register.filter()
def censor(text):
    # text is the objects which is treated by filter.
    
    # here we write out filter engine.
    # in our case, this replase rude words in title and article with
    # masked form like first letters and stars instead of other letters
    # f*** for example
    # filter called from template like {{ title|censor}}

    # for word in ILLEGAL_WORDS:
    #     pattern = re.compile(re.escape(word), re.IGNORECASE)
    #     text = pattern.sub('*' * len(word), text)

    words = text.split()
    for i in range(len(words)):
        for word in ILLEGAL_WORDS:
            if re.search(word, words[i].lower()) is not None:
            # if word in words[i].lower():
                words[i] = words[i].replace(words[i], words[i][0] + '*' * (len(words[i]) - 1))
                break
    return ' '.join(words)

    # kind of replacing procedure
    #     
    # we return the treated text by the filter
    return f'{text}'