from OpinionMining.models import Twitter
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
from .twitter import TwitterClient


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request, exception):
    return render(request, '500.html', status=500)


# Logout view
def logout(request):
    messages.success(request, "Successfully Logged out :)")
    auth.logout(request)
    return redirect('login')


def getUsersname(request):
    data = list(map(lambda x: x.username, User.objects.all()))
    return HttpResponse(json.dumps(data), content_type="application/json")


def getEmaillist(request):
    data = list(map(lambda x: x.email, User.objects.all()))
    return HttpResponse(json.dumps(data), content_type="application/json")


def about(request):
    return render(request, 'about.html', {'title': 'About'})

def privacy(request):
    return render(request, 'privacy.html', {'title': 'Privacy Policy'})

def login(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = auth.authenticate(username=u, password=p)

        if user is not None:
            auth.login(request, user)
            google = user.socialaccount_set.filter(provider='google')
            if google:
                google[0].extra_data['picture']
            messages.success(request, f'Welcome {u}')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'registration/login.html', {'title': 'Login'})


def register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email is already taken by others')
                return redirect('register')
            elif User.objects.filter(username=uname):
                messages.error(request, 'Username is taken by others')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=uname, email=email, password=password1)
                messages.success(request, 'Registration Success!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords does not match :(')
            return redirect('register')

    else:
        return render(request, 'register.html', {'title': 'Register'})


@login_required(login_url='login')
def getjobv(request):
    form = postjob.objects.all().exclude(jobposter=request.user)
    context = {
        'form': form
    }
    return render(request, 'main/getjob.html', context)


def home(request):
    return render(request, 'index.html', {'title': 'Home'})


@csrf_exempt
def analyze(request):
    if request.is_ajax():
        hashtag = request.POST.get('hashtag')
        twitter_data = get_data(hashtag)
        labels = [
            'Positive',
            'Negative',
            'Neutral'
        ]
        chartLabel = ["Percentage"]
        chartdata = [twitter_data['ptweet_percent'],
                     twitter_data['ntweet_percent'], twitter_data['neutral_percent']]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }
        twitter_data.update(data)
        twitter_obj=Twitter()
        twitter_obj.user = request.user
        twitter_obj.json_data= json.dumps(twitter_data)
        return HttpResponse(json.dumps(twitter_data), content_type="application/json")


def get_data(tag, data={}):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=tag)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets[:-1]
               if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    data['data_dict'] = tweets[-1]
    data['ptweet_percent'] = 100*len(ptweets)/len(tweets)
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets[:-1]
               if tweet['sentiment'] == 'negative']
    neutral = [tweet for tweet in tweets[:-1]
               if tweet['sentiment'] == 'neutral']
    data['ntweet_percent'] = 100*len(ntweets)/len(tweets)
    data['neutral_percent'] = 100 * \
        (len(tweets) - (len(ntweets)+len(ptweets)))/len(tweets)
    return data
