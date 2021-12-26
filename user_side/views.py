from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from user_side.forms import SearchForm
from worker_side.models import Book

def home(request):
    return render(request, "user_side/home.html")

def search(request):

    if 'title' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            context = {
                'title': f"Search results for {form.cleaned_data['title']} - Online Library Catalog",
                'results': Book.objects.filter(title__contains=form.cleaned_data['title'])[0].author.all()[0].name
            }

        return render(request, "user_side/search.html", context)
    else:
        return redirect("user_side-home")

def log_in(request):
    return render(request, "user_side/log_in.html")

@login_required
def profile(request):
    return render(request, "user_side/profile.html")