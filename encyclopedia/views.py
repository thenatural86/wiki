from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2


class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia', 'style': 'width:100%'}))


class NewForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Create Title'}))
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Enter a Description', 'style': 'height: 40%'}))


class EditForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Create Title'}))
    data = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Enter a Description', 'style': 'height: 40%'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def entry(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry),
        "form": SearchForm()
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
    if request.method == "POST":
        new_entry = NewForm(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data["title"]
            content = new_entry.cleaned_data["content"]
            entries_all = util.list_entries()
            for entry in entries_all:
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/new.html", {
                        "form": SearchForm(),
                        "newForm": NewForm(),
                        "error": "That title already exist!"
                    })
            new_title = "# " + title
            new_content = "\n" + content
            new_data = new_title + new_content
            util.save_entry(title, new_data)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(entry),
                "form": SearchForm()
            })
    return render(request, "encyclopedia/new.html", {
        "form": SearchForm(),
        "newForm": NewForm()
    })


def edit(request, title):
    if request.method == "POST":
        edit_entry = EditForm(request.POST)
        if edit_entry.is_valid():
            title = edit_entry.cleaned_data["title"]
            data = edit_entry.cleaned_data["data"]
            util.save_entry(title, data)
            entry = util.get_entry(title)
            print("POSTING")
            return HttpResponseRedirect(reverse("entry", args=[title]))
            # return render(request, "encyclopedia/entry.html", {
            #     "title": title,
            #     "entry": markdown2.markdown(entry),
            #     "form": SearchForm()
            # })
    else:
        entry = util.get_entry(title)
        edit_form = EditForm(initial={'title': title, 'data': entry})
        print("GETTING")
        return render(request, "encyclopedia/edit.html", {
            # "title": title,
            "entry": entry,
            "edit_form": edit_form
        })
    # elif request.method == "POST":
    #     return HttpResponseRedirect(reverse("entry", args=[title]))
