from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
import sys


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def title(request,title):
    entry=util.get_entry(title)
    markdowner=Markdown()
    if title not in util.list_entries():
        return HttpResponse("No Such Page Available")
    return render(request,"encyclopedia/title.html",{
    "content":markdowner.convert(entry),
    "title": title
    })
def search(request):

    data=request.GET.get("search")
    lst=util.list_entries()
    markdowner=Markdown()
    var=0

    if data in lst:
        return HttpResponseRedirect(reverse("title", kwargs={"title":data}))
        var=1
        sys.exit()

    for i in lst:
        if data in i:
            return render(request,"encyclopedia/search2.html",{
            "result":i
            })
            var=1

    if var==0:
        return HttpResponse("No Result Found")



def create(request):

    if request.method=="POST":
        create_content=request.POST.get("create_content")
        create_title=request.POST.get("create_title")

        if create_title not in util.list_entries():
            util.save_entry(create_title,create_content)
            return HttpResponseRedirect(reverse("index"))

        else:
            return HttpResponse("Title Already Exists")

    return render(request,"encyclopedia/create.html")

def edit(request,title):
    edit_content=request.POST.get("edit_content")
    if request.method=="POST":
        util.save_entry(title,edit_content)
        return HttpResponseRedirect(reverse("title",kwargs={'title': title}))
        sys.exit()
    markdowner=Markdown()
    content=util.get_entry(title)
    return render(request,"encyclopedia/edit.html",{
    "content":content
    })
