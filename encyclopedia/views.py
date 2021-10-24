import os
import random
import markdown2
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


class NewArticleForm(forms.Form):
    pholder = "Input text in Markdowm format"
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'size': 80}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': pholder}))


class ArticleEditForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/article.html", {
            "name": name,
            "entry": markdown2.markdown(util.get_entry(name))
            })
    else:
        return render(request, "encyclopedia/error.html", {
            "name": name
            })


def random_article(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("article", kwargs={'name': entry}))


def search(request):
    query = request.GET.get('q')
    if query in util.list_entries():
        return HttpResponseRedirect(reverse("article", kwargs={'name': query}))
    else:
        search_results = []
        for entry in util.list_entries():
            if query in entry:
                search_results.append(entry)
        if not search_results:
            empty = "There were no results matching the query."
        else:
            empty = ""
        return render(request, "encyclopedia/search.html", {
            "search_results": search_results,
            "empty": empty
            })


def add(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            new_article_path = "entries/" + title +".md"
            if not os.path.exists(new_article_path):
                with open(new_article_path, "w") as new_article:
                    new_article.write(content)
            else:
                return render(request, "encyclopedia/exist.html", {
                    "title": title
                })
            return HttpResponseRedirect(reverse("article", kwargs={'name': title}))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })               
    return render(request, "encyclopedia/add.html", {
        "form": NewArticleForm()
        })


def edit(request, name):
    if request.method == "POST":
        form = ArticleEditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            article_path = "entries/" + name +".md"
            with open(article_path, "w") as article:
                article.write(content)
            return HttpResponseRedirect(reverse("article", kwargs={'name': name}))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": name
                }) 
    initial_content = util.get_entry(name)
    form = ArticleEditForm(initial={'content': initial_content})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": name
        })
