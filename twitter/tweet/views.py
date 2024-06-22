from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Tweet
from .forms import TweetForm 
# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('created_at')