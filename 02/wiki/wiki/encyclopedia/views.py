from django.shortcuts import render, redirect
from . import util
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import choice


class NewPageForm(forms.Form):
    title = forms.CharField(label='Title',widget=forms.TextInput(attrs={'placeholder': 'The title'}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 10, 'cols': 150,
    'placeholder': 'The markdown', 'style': 'height: auto;'}))

def index(request):
    msg=request.GET.get('q')
    if msg:
        if util.get_entry(msg):
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown2.markdown(util.get_entry(msg)), "title": msg.capitalize()
            })
        results = []
        for entries in util.list_entries():
            if msg.lower() in entries.lower():
                results.append(entries)
        return render(request, "encyclopedia/search.html", {
            "results": results
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, q):
    print("hi0",q)    
    if util.get_entry(q):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(q)), "title": q
        })
    return render(request, "encyclopedia/error.html", {
        "title": q
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title.lower() in (entries.lower() for entries in util.list_entries()):
                return render(request, "encyclopedia/error_new.html", {
                    "title": title
                })
            util.save_entry(title, text)
            return redirect(f"wiki/{title}")

    form = NewPageForm()
    return render(request, "encyclopedia/new.html", {
        "form": form
    })

def edit_page(request, q):
    print("hi1",q)
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return redirect(f"../wiki/{title}")
    if util.get_entry(q):
        form = NewPageForm()
        form.fields["title"].initial = q
        form.fields["text"].initial = util.get_entry(q)
        form.fields['title'].widget = forms.HiddenInput()
        return render(request, "encyclopedia/edit.html", {
            "form": form, "title": q
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": q
        })

def random_page(request):
    pages = util.list_entries()
    page = choice(pages)
    return redirect(f"wiki/{page}")