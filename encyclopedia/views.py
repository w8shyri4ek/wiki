from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util

def converting(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def greet(request, title):
    title_content = converting(title)
    if title_content == None:
        return render(request,"encyclopedia/error.html",{"message": "Not found"})
    else:
        return render(request,"encyclopedia/page.html",{"title":title,"content":title_content})
def search(request):
    if request.method == "POST":
        input_search = request.POST['q']
        html_search = converting(input_search)
        if html_search is not None:
            return render(request, "encyclopedia/page.html", {"title":input_search, "content":html_search})
        else:
            allEntries = util.list_entries()
            options = []
            for entry in allEntries:
                if input_search.lower() in entry.lower():
                    options.append(entry)
            return render(request, "encyclopedia/search.html", {"options":options})
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        header = request.POST['header']
        content = request.POST['content']
        getEntries = util.get_entry(header)
        if getEntries is not None:
            return render(request, "encyclopedia/error.html", {"message":"entry already exists"})
        else:
            util.save_entry(header,content)
            html_content = converting(header)
            return render(request,"encyclopedia/page.html", {"title":header, "content":html_content})
def edit_page(request):
    if request.method == 'POST':
        title = request.POST['edit_btn']
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit_page.html", {"title": title, "content": content})
def save_edit_page(request):
    if request.method == 'POST':
        title = request.POST['header']
        content = request.POST['content']
        util.save_entry(title,content)
        html_content = converting(title)
        return render(request,"encyclopedia/page.html", {"titli":title, "content":html_content})
def random_page(request):
    allEntries = util.list_entries()
    random_choice_page = random.choice(allEntries)
    html_content = converting(random_choice_page)
    return render(request,"encyclopedia/page.html", {"title": random_choice_page, "content":html_content})