from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from app01 import models
from django import forms


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


def depart_edit(request, nid):
    if request.method == "GET":
        row = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row': row})
    models.Department.objects.filter(id=nid).update(title=request.POST.get("title"))
    return redirect("/depart/list/")


def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'users': queryset})


class UserModeForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'age', 'password', 'account', 'depart']


def user_add(request):
    if request.method == "GET":
        form = UserModeForm()
        return render(request, 'user_add.html', {'form': form})
    form = UserModeForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")


def user_edit(request, nid):
    if request.method == "GET":
        row = models.UserInfo.objects.filter(id=nid).first()
        form = UserModeForm(instance=row)
        return render(request, 'user_edit.html', {"form": form})
    row = models.UserInfo.objects.filter(id=nid).first()
    form = UserModeForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def prettynum_list(request):
    queryset = models.PrettyNum.objects.all().order_by('-level')
    return render(request, 'PrettyNum_list.html', {'users': queryset})


class PrettyNumForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) != 11:
            raise ValidationError('nm')
        return mobile


def prettynum_add(request):
    if request.method == "GET":
        form = PrettyNumForm()
        return render(request, 'prettynum_add.html', {'form': form})
    form = PrettyNumForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/PrettyNum/list/")
    return render(request, 'prettynum_add.html', {'form': form})
