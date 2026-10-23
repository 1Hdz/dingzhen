from django.shortcuts import render, redirect
from app01 import models
from app01.forms import UserModelForm, PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import Pagination


# ============ 部门管理 ============
def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')


def depart_delete(request, aid):
    models.Department.objects.filter(id=aid).delete()
    return redirect('/depart/list/')


def depart_edit(request, aid):
    row = models.Department.objects.filter(id=aid).first()
    if request.method == 'GET':
        return render(request, 'depart_edit.html', {'row': row})
    title = request.POST.get('title')
    models.Department.objects.filter(id=aid).update(title=title)
    return redirect('/depart/list/')


# ============ 用户管理 ============
def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    """原生表单方式（user_add.html）"""
    if request.method == 'GET':
        gender_choices = models.UserInfo.gender_choices
        depart_list = models.Department.objects.all()
        return render(request, 'user_add.html', {'gender_choices': gender_choices, 'depart_list': depart_list})
    name = request.POST.get('user')
    password = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    create_time = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')
    models.UserInfo.objects.create(
        name=name,
        password=password,
        age=age,
        account=account,
        create_time=create_time,
        gender=gender,
        depart_id=depart_id,
    )
    return redirect('/user/list/')


def user_model_form_add(request):
    """ModelForm方式（user_model_form_add.html）"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_model_form_add.html', {'form': form})


def user_edit(request, uid):
    row = models.UserInfo.objects.filter(id=uid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row)
        return render(request, 'user_edit.html', {'form': form})
    form = UserModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, uid):
    models.UserInfo.objects.filter(id=uid).delete()
    return redirect('/user/list/')


# ============ 靓号管理 ============
def pretty_list(request):
    q = request.GET.get('q', '')
    queryset = models.PrettyNum.objects.all().order_by('-level')
    if q:
        queryset = queryset.filter(mobile__contains=q)

    # 分页
    total_count = queryset.count()
    page = Pagination(request, total_count)
    queryset = queryset[page.start_index:page.end_index]

    return render(request, 'pretty_list.html', {'queryset': queryset, 'q': q, 'page_html': page.html()})


def pretty_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, pid):
    row = models.PrettyNum.objects.filter(id=pid).first()
    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row)
        return render(request, 'pretty_edit.html', {'form': form})
    form = PrettyEditModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, pid):
    models.PrettyNum.objects.filter(id=pid).delete()
    return redirect('/pretty/list/')
