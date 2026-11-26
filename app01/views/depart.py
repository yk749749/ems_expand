# app01/views/depart.py
"""部门管理视图。"""
from django.shortcuts import redirect, render

from app01 import models
from app01.utils.pagination import Pagination


def depart_list(request):
    """部门列表"""
    # 加上 order_by("id")，保证每次分页查询时数据顺序稳定
    queryset = models.Department.objects.all().order_by("id")

    # 实例化分页对象，每页显示 3 条
    page_object = Pagination(request, queryset, page_size=3)

    context = {
        "queryset": page_object.page_queryset,  # 分好页的数据
        "page_string": page_object.html(),  # 生成的分页 HTML 按钮
    }
    return render(request, "depart_list2.html", context)


def depart_add(request):
    """新建部门"""
    # GET 请求：打开新建页面
    if request.method == "GET":
        return render(request, "depart_add2.html")

    # POST 请求：获取标题并保存到数据库
    title = request.POST.get("title")
    models.Department.objects.create(title=title)

    # 重定向回部门列表页面
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    # 获取前端通过 URL 传递过来的 id
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()

    # 删除完成后，重定向回部门列表页面
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """编辑部门"""
    # GET 请求：打开编辑页面并回显数据
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit2.html", {"row_object": row_object})

    # POST 请求：更新数据库中的记录
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)

    # 更新完成后，重定向回部门列表页面
    return redirect("/depart/list/")


def depart_multi(request):
    """ 批量导入部门（Excel文件）"""
    from openpyxl import load_workbook

    # 1. 获取用户上传的文件对象
    file_object = request.FILES.get("exc")

    # 没有选择文件时直接返回列表页，避免 AttributeError
    if not file_object:
        return redirect("/depart/list/")

    # 2. 对象传递给openpyxl，由openpyxl读取文件的内容
    wb = load_workbook(file_object)
    sheet = wb.worksheets[0]

    # 3. 循环获取每一行数据（第 1 行是表头，从第 2 行开始读）
    for row in sheet.iter_rows(min_row=2):
        text = row[0].value
        if text is None:
            continue
        text = str(text).strip()
        if not text:
            continue

        exists = models.Department.objects.filter(title=text).exists()
        if not exists:
            models.Department.objects.create(title=text)

    return redirect('/depart/list/')
