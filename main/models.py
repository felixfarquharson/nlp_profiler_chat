from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Message(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)


class LastSeen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    sentences_count = models.FloatField()
    characters_count = models.FloatField()
    repeated_letters_count = models.FloatField()
    spaces_count = models.FloatField()
    chars_excl_spaces_count = models.FloatField()
    repeated_spaces_count = models.FloatField()
    whitespaces_count = models.FloatField()
    chars_excl_whitespaces_count = models.FloatField()
    repeated_whitespaces_count = models.FloatField()
    count_words = models.FloatField()
    duplicates_count = models.FloatField()
    emoji_count = models.FloatField()
    repeated_digits_count = models.FloatField()
    whole_numbers_count = models.FloatField()
    alpha_numeric_count = models.FloatField()
    non_alpha_numeric_count = models.FloatField()
    punctuations_count = models.FloatField()
    repeated_punctuations_count = models.FloatField()
    stop_words_count = models.FloatField()
    dates_count = models.FloatField()
    noun_phase_count = models.FloatField()
    english_characters_count = models.FloatField()
    non_english_characters_count = models.FloatField()
    sentiment_polarity_score = models.FloatField()
    sentiment_subjectivity_score = models.FloatField()
    grammar_check_score = models.FloatField()
    spelling_quality_score = models.FloatField()
    ease_of_reading_score = models.FloatField()
