from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.db.models.functions import TruncDay, Concat
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_pandas.io import read_frame

from main.forms import SignupForm
from main.models import Profile, Message, LastSeen


def home(request):
    msg_days = Profile.objects.annotate(created=F("message__created")).annotate(date=TruncDay("created")).values(
        "date").annotate(c=Count("id")).values("date", "c")[:7]
    return render(request, "home.html", {"days": msg_days})


def report_msg(request, year, month, day, user, msg_id):

    objs = Profile.objects.filter(message_id=msg_id)

    if len(objs)!=1:
        return HttpResponseNotFound()

    df = read_frame(objs)
    graphs = []
    graphs += [{"title": 'Sentence and Word Counts', "html": df[["sentences_count", "count_words"]].to_html()}]

    graphs += [{"title": 'Spaces and Whitespace Counts', "html": df[["spaces_count", "whitespaces_count"]]
            .to_html()}]

    graphs += [{"title": 'Character Counts',
                "html": df[["characters_count", "chars_excl_spaces_count", "chars_excl_whitespaces_count"]]
            .to_html()}]

    graphs += [{"title": 'Repeats Counts', "html": df[["repeated_letters_count", "repeated_digits_count",
                                                       "repeated_spaces_count","repeated_whitespaces_count"]]
            .to_html()}]

    graphs += [{"title": 'Emojis, Numbers, Punctuation and Dates Counts',
                "html": df[["emoji_count", "whole_numbers_count", "punctuations_count", "dates_count"]]
            .to_html()}]

    graphs += [
        {"title": 'Duplicates Counts', "html": df[["duplicates_count", "repeated_punctuations_count"]]
            .to_html()}]

    graphs += [{"title": 'Alpha Numeric and Non Alpha Numeric Counts',
                "html": df[["alpha_numeric_count", "non_alpha_numeric_count"]]
            .to_html()}]

    graphs += [
        {"title": 'Stop Words and Nouns Counts', "html": df[["stop_words_count", "noun_phase_count"]]
            .to_html()}]

    graphs += [{"title": 'English and Non English Counts',
                "html": df[["english_characters_count", "non_english_characters_count"]].to_html()}]

    graphs += [{"title": 'Sentiment Scores',
                "html": df[["sentiment_polarity_score", "sentiment_subjectivity_score"]].to_html()}]

    graphs += [{"title": 'Grammar, Spelling and Ease of Reading Scores',
                "html": df[["grammar_check_score", "spelling_quality_score", "ease_of_reading_score"]]
        .to_html()}]

    context = {"graphs": graphs, "user": user, "msg": objs[0].message.body, "year": year, "month": month, "day": day}
    return render(request, "report_msg.html", context)


def _graphs(qs, user=None):

    df = read_frame(qs)
    graphs = []
    graphs += [{"title": 'Sentence and Word Counts', "html": df.describe()[["sentences_count", "count_words"]]
        .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Spaces and Whitespace Counts', "html": df.describe()[["spaces_count", "whitespaces_count"]]
        .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Character Counts',
                "html": df.describe()[["characters_count", "chars_excl_spaces_count", "chars_excl_whitespaces_count"]]
                    .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Repeats Counts', "html": df.describe()[["repeated_letters_count", "repeated_digits_count",
                                                                  "repeated_spaces_count",
                                                                  "repeated_whitespaces_count"]]
        .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Emojis, Numbers, Punctuation and Dates Counts',
                "html": df.describe()[["emoji_count", "whole_numbers_count", "punctuations_count", "dates_count"]]
                    .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Duplicates Counts', "html": df.describe()[["duplicates_count", "repeated_punctuations_count"]]
        .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Alpha Numeric and Non Alpha Numeric Counts',
                "html": df.describe()[["alpha_numeric_count", "non_alpha_numeric_count"]]
                    .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Stop Words and Nouns Counts', "html": df.describe()[["stop_words_count", "noun_phase_count"]]
        .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'English and Non English Counts',
                "html": df.describe()[["english_characters_count", "non_english_characters_count"]]
                    .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Sentiment Scores', "html": df.describe()[["sentiment_polarity_score",
                                                                    "sentiment_subjectivity_score"]]
        .transpose()[["mean", "min", "max"]].transpose().to_html()}]

    graphs += [{"title": 'Grammar, Spelling and Ease of Reading Scores',
                "html": df.describe()[["grammar_check_score", "spelling_quality_score", "ease_of_reading_score"]]
                    .transpose()[["mean", "min", "max"]].transpose().to_html()}]


    users = []
    messages = []
    for obj in qs:
        if obj.message.user.username not in users:
            users += [obj.message.user.username]
        messages += [{"id": obj.message.pk, "time": obj.message.created, "body": obj.message.body}]

    context = {"graphs": graphs, "users": users}
    if user:
        context["user"] = user
        context["messages"] = messages

    return context


def report_user(request, year, month, day, user):

    objs = Profile.objects.filter(message__created__year=year, message__created__month=month,
                                  message__created__day=day, message__user__username=user)

    if not len(objs)>=1:
        return HttpResponseNotFound()

    context = _graphs(objs, user)
    context.update({"year": year, "month": month, "day": day})

    return render(request, "report_user.html", context=context)


def report(request, year, month, day):
    objs = Profile.objects.filter(message__created__year=year, message__created__month=month,
                                  message__created__day=day)
    if not len(objs)>=1:
        return HttpResponseNotFound()

    context = _graphs(objs)
    context.update({"year": year, "month": month, "day": day})
    return render(request, "report.html", context=context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



@login_required
def livechat(request):
    return render(request, "livechat.html")


@login_required
def api_lc_messages(request):
    if LastSeen.objects.filter(user=request.user).exists():
        lasts = LastSeen.objects.get(user=request.user)
        lasts.datetime = timezone.now()
        lasts.save()
    else:
        LastSeen(user=request.user).save()
    online = LastSeen.objects.filter(datetime__gte=timezone.now() - timedelta(seconds=60))\
        .annotate(username=F('user__username'))\
        .values("username").order_by("username")
    online = [x["username"] for x in online]
    newest_hundred = Message.objects.filter(deleted=False).order_by("created")[:100]
    recent_msgs = []
    for message in newest_hundred:
        recent_msgs += [{"id": message.pk, "datetime": message.created, "username": message.user.username,
                         "user": message.user.username, "body": message.body}]
    return JsonResponse({"messages": recent_msgs, "online": online})


@login_required
@csrf_exempt
def api_lc_add(request):
    if request.method == "POST":
        Message(body=request.POST['body'], user=request.user).save()
        return JsonResponse({"status": "done"})
    return JsonResponse({"status": "failed: not post"})


@login_required
@csrf_exempt
def api_lc_delete(request):
    if request.method == "POST":
        if request.POST['del']:
            if not Message.objects.filter(pk=request.POST['del']).exists():
                return JsonResponse({"status": "failed: wrong id"})
            msg = Message.objects.get(pk=request.POST["del"])
            if msg.user != request.user:
                return JsonResponse({"status": "failed: not your post"})
            if msg.deleted:
                return JsonResponse({"status": "failed: already deleted"})
            msg.deleted=True
            msg.save()
            return JsonResponse({"status": "done"})
        return JsonResponse({"status": "failed: no id provided"})
    return JsonResponse({"status": "failed: not post"})