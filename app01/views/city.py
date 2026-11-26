# app01/views/city.py
"""城市列表：FileField + MEDIA 的使用示例。"""
from django.shortcuts import redirect, render

from app01 import models
# 复用 20.3 中针对 City 的 ModelForm，避免同一个表单写两遍
from app01.views.upload import UpModelForm


def city_list(request):
    """城市列表（展示 MEDIA 中的 Logo）"""
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})


def city_add(request):
    """新建城市：FileField 由 ModelForm 自动保存到 MEDIA_ROOT/city/"""
    title = "新建城市"

    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")
    return render(request, 'upload_form.html', {"form": form, 'title': title})
