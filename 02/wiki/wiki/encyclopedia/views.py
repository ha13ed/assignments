from django.shortcuts import render
from . import util
import markdown2
from django import forms


class NewQueryForm(forms.Form):
    Query = forms.CharField()


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
        "entries": util.list_entries(), "form": NewQueryForm()
    })


def entry(request, q):
    if util.get_entry(q):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(q)), "title": q.capitalize()
        })
    return render(request, "encyclopedia/entry.html", {
        "entry": "Page Was Not Found", "title": "Page Not Found!"
    })
