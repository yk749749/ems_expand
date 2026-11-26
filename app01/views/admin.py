# app01/views/admin.py
"""管理员管理视图。"""
from django.shortcuts import redirect, render

from app01 import models
from app01.utils.form import AdminEditForm, AdminModelForm, AdminResetPasswordForm
from app01.utils.pagination import Pagination


def admin_list(request):
    """管理员列表 & 搜索 & 分页"""
    # 1. 构建搜索条件
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 2. 获取符合条件的管理员数据
    queryset = models.Admin.objects.filter(**data_dict).order_by("id")

    # 3. 分页，每页显示 10 条
    page_object = Pagination(request, queryset, page_size=10)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        # 只有一条数据时也显示分页栏，保持界面完整
        "page_string": page_object.html(always_show=True),
    }
    return render(request, "admin_list.html", context)


def admin_add(request):
    """新建管理员"""
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    # POST 请求：校验并保存（密码在表单 save() 中转换为 MD5）
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    """编辑管理员（只修改用户名，不允许修改密码）"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request):
    """删除管理员"""
    nid = request.GET.get("nid")
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset_password(request, nid):
    """重置管理员密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    if request.method == "GET":
        form = AdminResetPasswordForm(instance=row_object)
        return render(
            request,
            "change.html",
            {"form": form, "title": f"重置密码 - {row_object.username}"},
        )

    form = AdminResetPasswordForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(
        request,
        "change.html",
        {"form": form, "title": f"重置密码 - {row_object.username}"},
    )
