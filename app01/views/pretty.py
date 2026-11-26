# app01/views/pretty.py
"""靓号管理视图。"""
from django.shortcuts import redirect, render

from app01 import models
from app01.utils.form import PrettyModelForm
from app01.utils.pagination import Pagination


def pretty_list(request):
    """靓号列表 & 搜索 & 分页"""
    # 1. 构建搜索条件
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 2. 获取所有符合搜索条件的数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 3. 实例化分页对象（传入 request 和 queryset），每页显示 3 条
    page_object = Pagination(request, queryset, page_size=3)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分好页的数据
        "page_string": page_object.html(),  # 生成的分页 HTML 按钮
    }
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """新建靓号"""
    # GET 请求：打开新建页面
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # POST 请求：校验并保存
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """编辑靓号"""
    # 根据 ID 获取要编辑的那一行数据
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        # 传入 instance 实现数据回显
        form = PrettyModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    # 提交修改：同时传入 instance 告知 Django 更新的是哪条数据
    form = PrettyModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request):
    """删除靓号"""
    # 获取前端通过 URL 传递过来的 id
    nid = request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()

    # 删除完成后，重定向回靓号列表页
    return redirect("/pretty/list/")
