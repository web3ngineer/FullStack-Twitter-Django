from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q



# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    # tweets = Tweet.objects.all().order_by('-created_at')
    # return render(request, 'tweet_list.html', {'tweets': tweets})
    
    page_number = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 8))

    # Calculate the starting point (offset)
    offset = (page_number - 1) * limit

    # Query the database with limit and offset
    tweets = Tweet.objects.all().order_by('-created_at')[offset:offset + limit]

    # Calculate the total number of pages
    total_tweets = Tweet.objects.count()
    total_pages = (total_tweets + limit - 1) // limit  

    context = {
        'tweets': tweets,
        'page_number': page_number,
        'total_pages': total_pages,
        'limit': limit,
    }

    return render(request, 'tweet_list.html', context)

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})


from django.core.paginator import Paginator

def search_results(request):
    query = request.GET.get('query')
    if query:
        results = Tweet.objects.filter(Q(text__icontains=query))
    else:
        results = Tweet.objects.none()  
        
    # Paginate the results
    paginator = Paginator(results, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'search_results.html', {'page_obj': page_obj, 'query': query})