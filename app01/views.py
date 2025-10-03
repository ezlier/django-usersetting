from django.shortcuts import render, redirect
from app01 import models


# Create your views here.
def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'departments': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def depart_edit(request,nid):
    if request.method == "GET":
        row = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row': row})
    models.Department.objects.filter(id=nid).update(title=request.POST.get("title"))
    return redirect("/depart/list/")