from django.http import HttpResponse
from django.shortcuts import render
import markdown

from . import util

def markdownconverter(title):
    md = util.get_entry(title)
    markdowner = markdown.Markdown()
    if md == None:
        return None
    else:
        return markdowner.convert(md)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    converted_html = markdownconverter(title)
    if converted_html == None:
            return render(request, "encyclopedia/error.html", {
                "message": "There is no matching entry available!"
            })
    else:
        return render(request,"encyclopedia/entry.html", {
            "title": title,
            "content": converted_html
        })

def search(request):
    if request.method == "POST":
        searchedentry = request.POST['q']
        converted_html = markdownconverter(searchedentry)
        if converted_html is not None:
            return render(request,"encyclopedia/entry.html", {
                "title": searchedentry,
                "content": converted_html
            })
        else:
            suggestedentries = []
            listedentries = util.list_entries()
            for entry in listedentries:
                if searchedentry.lower() in entry.lower():
                    suggestedentries.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "recommendation": suggestedentries
                })