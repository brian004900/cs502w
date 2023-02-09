from pdb import post_mortem
from django.shortcuts import render, redirect
from django import forms
from markdown2 import markdown
from random import sample
from django.http import HttpResponse
from . import util

class addform(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(label = "content", widget=forms.Textarea)

class editform(forms.Form):
    content = forms.CharField(label = "Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia\index.html", {
        "entries": util.list_entries()
    })

def add(request):
    if request.method == "POST":
        form = addform(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = request.POST.get("title").strip()
            content = request.POST.get("content").strip()
            if title in entries:
                 return HttpResponse('error')
            else:
                util.save_entry(title,content)
                return redirect("inpage", title=title)
    return render(request, "encyclopedia\\add.html",{"form":addform()} )

def inpage(request, title):
    cons  = util.get_entry(title)
    if cons is None:
        return render(request, "encyclopedia\error.html", )
    else:
        content = util.get_entry(title.strip())
        content = markdown(content)
        return render(request, "encyclopedia\inpage.html", {'content': content, 'title': title})

def search(request):
    q = request.GET.get('q').strip()
    if util.get_entry(q) != None:
        return redirect("inpage", title=q)
    else:
        entries=[] 
        for i in util.list_entries():
            if q.upper() in i.upper():
                entries.append(i)

        return render(request, "encyclopedia\search.html", {
        "entries": entries, "q": q})

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)

    if request.method == "POST":
        form = editform(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('inpage',title=title)
    return render(request, "encyclopedia\edit.html", {"form":editform(initial={'content':content}), 
    "title":title})

def random(request):
    titles = util.list_entries()
    random_title = sample(titles,1)
    title = random_title[0]
    return redirect('inpage', title=title)