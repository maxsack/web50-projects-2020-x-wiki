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
        searchentry = request.POST['q']
        converted_html = markdownconverter(searchentry)
        if converted_html is not None:
            return render(request,"encyclopedia/entry.html", {
                "title": searchentry,
                "content": converted_html
            })
        else:
            return render(request, "encyclopedia/searchresult.html")