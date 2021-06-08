#!/usr/bin/env python3
from datetime import timedelta

from django.utils import timezone
from django_pandas.io import read_frame
from nlp_profiler.core import apply_text_profiling

from django.conf import settings
import djangoProject.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS, DATABASES=app_settings.DATABASES,
                   SECRET_KEY=app_settings.SECRET_KEY)

import django

django.setup()

from main.models import Message, Profile

yesterday = timezone.now() - timedelta(days=1)
messages = Message.objects.filter(created__year=yesterday.year, created__month=yesterday.month,
                                  created__day=yesterday.day)
frame = read_frame(messages)
processed_frame = apply_text_profiling(frame, "body", {'grammar_check': True})

print(processed_frame)
def msganditem():
    for i in range(len(processed_frame)):
        yield messages[i], processed_frame.loc[i]


for message, item in msganditem():
    print(message, item)
    Profile(message=message, sentences_count=item['sentences_count'],
                           characters_count=item['characters_count'],
                           repeated_letters_count=item['repeated_letters_count'], spaces_count=item['spaces_count'],
                           chars_excl_spaces_count=item['chars_excl_spaces_count'],
                           repeated_spaces_count=item['repeated_spaces_count'],
                           whitespaces_count=item['whitespaces_count'],
                           chars_excl_whitespaces_count=item['chars_excl_whitespaces_count'],
                           repeated_whitespaces_count=item['repeated_whitespaces_count'],
                           count_words=item['count_words'],
                           duplicates_count=item['duplicates_count'], emoji_count=item['emoji_count'],
                           repeated_digits_count=item['repeated_digits_count'],
                           whole_numbers_count=item['whole_numbers_count'],
                           alpha_numeric_count=item['alpha_numeric_count'],
                           non_alpha_numeric_count=item['non_alpha_numeric_count'],
                           punctuations_count=item['punctuations_count'],
                           repeated_punctuations_count=item['repeated_punctuations_count'],
                           stop_words_count=item['stop_words_count'], dates_count=item['dates_count'],
                           noun_phase_count=item['noun_phase_count'],
                           english_characters_count=item['english_characters_count'],
                           non_english_characters_count=item['non_english_characters_count'],
                           sentiment_polarity_score=item['sentiment_polarity_score'],
                           sentiment_subjectivity_score=item['sentiment_subjectivity_score'],
                           grammar_check_score=item['grammar_check_score'],
                           spelling_quality_score=item['spelling_quality_score'],
                           ease_of_reading_score=item['ease_of_reading_score']).save()
