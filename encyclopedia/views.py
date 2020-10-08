from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse


class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia', 'style': 'width:100%'}))


class NewForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Create Title'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": util.get_entry(title)
    })


def search(request):
    entries_found = []
    entries_all = util.list_entries()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            for entry in entries_all:
                query = form.cleaned_data["query"].lower()
                entry = entry.lower()
                if query == entry:
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("entry", args=[title]))
                if query in entry:
                    entries_found.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "query": query,
                "form": SearchForm()
            })
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": SearchForm()
    })


def new(request):
    return render(request, "encyclopedia/new.html", {
        "form": SearchForm(),
        "newForm": NewForm()
    })
