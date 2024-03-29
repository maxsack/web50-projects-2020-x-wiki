from django.http import HttpResponse
from django.shortcuts import render
import markdown
import random

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
        query = request.POST['q']
        converted_html = markdownconverter(query)
        if converted_html is not None:
            return render(request,"encyclopedia/entry.html", {
                "title": query,
                "content": converted_html
            })
        else:
            entries = util.list_entries()
            suggestedentries = []
            for entry in entries:
                if query.lower() in entry.lower():
                    suggestedentries.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": suggestedentries
            })

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        body_content = request.POST['body']
        existingentries = util.get_entry(title)
        if existingentries is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Such an entry already exists!"
            })
        else: 
            util.save_entry(title, body_content)
            converted_html = markdownconverter(title)
            return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": converted_html
        })

def editpage(request):
    if request.method == "POST":
        title = request.POST['entrytitle']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
        })
    else:
        return

def saveedit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['body']
        util.save_entry(title, content)
        converted_html = markdownconverter(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": converted_html
        })
    else:
        return

def randompage(request):
    entries = util.list_entries()
    randomentry = random.choice(entries)
    converted_html = markdownconverter(randomentry)
    return render(request, "encyclopedia/entry.html", {
        "title": randomentry,
        "content": converted_html
    })