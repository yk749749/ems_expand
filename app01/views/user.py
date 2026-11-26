# app01/views/user.py
"""用户管理视图。"""
from django.shortcuts import redirect, render

from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all().order_by("id")

    # 实例化分页对象，每页显示 3 条
    page_object = Pagination(request, queryset, page_size=3)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, "user_list.html", context)


def user_model_form_add(request):
    """添加用户（ModelForm 版本）"""
    # GET 请求：打开添加页面，传入空表单
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # POST 请求：提交数据并进行校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    # 校验失败，把带有错误信息的表单重新返回给页面
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    # 根据 ID 获取要编辑的那一行数据
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 传入 instance，Django 会自动在页面上回显默认数据
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    # 提交修改：传入 instance 告知 Django 更新的是哪条数据
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, "user_edit.html", {"form": form})


def user_delete(request):
    """删除用户"""
    # 获取前端通过 URL 传递过来的 id
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()

    # 删除完成后，重定向回用户列表页面
    return redirect("/user/list/")
