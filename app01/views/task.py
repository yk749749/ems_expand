# app01/views/task.py
"""任务管理视图：任务列表（表单 + 分页表格） + Ajax 演示 + Ajax 提交入库。"""
from django import forms
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootstrapModelForm):
    """任务表单：级别、标题、详细信息、负责人。"""

    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # 详细信息用多行文本框
            "detail": forms.Textarea(attrs={"rows": 4}),
        }


def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务（按 id 倒序，新建的排在最前）
    queryset = models.Task.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)

    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),      # 生成页码
    }
    return render(request, "task_list.html", context)


def task_ajax(request):
    """Ajax 学习演示接口：示例1/2/3 都打到这里，直接返回 JSON。"""
    # 打印收到的数据，便于教学观察
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    """真正的任务提交：Ajax 校验并入库。"""
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    # 校验失败：返回字段错误（ErrorDict/ErrorList 可被 json.dumps 序列化）
    return JsonResponse({"status": False, "error": form.errors})


def task_edit(request, nid):
    """编辑任务（GET 回显数据，POST 校验并保存）"""
    row_object = models.Task.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/task/list/")

    if request.method == "GET":
        form = TaskModelForm(instance=row_object)
        return render(request, "task_edit.html", {"form": form, "row_object": row_object})

    form = TaskModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/task/list/")

    # 校验失败：带着错误重新渲染表单
    return render(request, "task_edit.html", {"form": form, "row_object": row_object})


def task_delete(request):
    """删除任务"""
    nid = request.GET.get("nid")
    models.Task.objects.filter(id=nid).delete()
    return redirect("/task/list/")
