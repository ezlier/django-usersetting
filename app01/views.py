from io import BytesIO
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01.utils.encrypt import md5
from app01 import models
from django import forms
from app01.utils.code import check_code


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
    # 建300条数据
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile=12345678765,price=i+20,level=2,status=1)

    data_dict = {}
    value = request.GET.get('data')
    if value:
        data_dict["mobile__contains"] = value
    else:
        value = ""

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    # 2. 分页核心逻辑
    page = request.GET.get('page', 1)  # 获取当前页码（默认为1）
    paginator = Paginator(queryset, 10)  # 每页显示10条数据

    try:
        page_obj = paginator.page(page)
    except Exception:
        page_obj = paginator.page(1)

    context = {
        'users': page_obj,  # 当前页数据
        'page_obj': page_obj,  # 页对象
        'paginator': paginator,  # 分页器本身（可获取页数等）
        'value': value,  # 搜索关键字，返回前端以便保留输入
    }
    return render(request, 'PrettyNum_list.html', context)


class PrettyNumForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # 校验
    # def clean_mobile(self):
    #     mobile = self.cleaned_data['mobile']
    #     if len(mobile) != 11:
    #         raise ValidationError('nm')
    #     return mobile


def prettynum_add(request):
    if request.method == "GET":
        form = PrettyNumForm()
        return render(request, 'prettynum_add.html', {'form': form})
    form = PrettyNumForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/PrettyNum/list/")
    return render(request, 'prettynum_add.html', {'form': form})


def prettynum_edit(request, nid):
    row = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyNumForm(instance=row)
        return render(request, 'prettynum_edit.html', {'form': form})
    form = PrettyNumForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/PrettyNum/list/")
    return render(request, 'prettynum_edit.html', {'form': form})


def prettynum_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/PrettyNum/list/")


def admin_list(request):
    info = request.session.get('info')
    if not info:
        return redirect("/login/")
    queryset = models.Admin.objects.all()
    context = {'admins': queryset}
    return render(request, 'admin_list.html', context)


class AdminForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    title = "添加管理员"
    if request.method == "GET":
        form = AdminForm()
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {'form': form})


def admin_edit(request, nid):
    row = models.Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        if not row:
            return redirect("/admin/list/")
        title = '编辑管理员'
        form = AdminForm(instance=row)
        return render(request, 'change.html', {'form': form, 'title': title})
    form = AdminForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {'form': form})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', 'error')
            return render(request, 'login.html', {'form': form})
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        request.session.set_expiry(60*60*24*7)
        return redirect("/admin/list/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect("/login/")


def image_code(request):
    img, code_string = check_code()
    request.session['image_code'] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())