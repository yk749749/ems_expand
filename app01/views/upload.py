# app01/views/upload.py
"""文件上传视图：原始方式 / 普通 Form / ModelForm / 头像预览。"""
import os

from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app01 import models
from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm


def upload_list(request):
    """原始方式：从 request.FILES 拿文件，用 chunks() 分块写盘（适合大文件）。"""
    if request.method == "GET":
        return render(request, "upload_list.html")

    file_object = request.FILES.get("avatar")
    if not file_object:
        return HttpResponse("请先选择要上传的文件")

    # 只取文件名，避免客户端传入 ../ 之类的路径
    filename = os.path.basename(file_object.name)
    file_path = os.path.join(settings.BASE_DIR, filename)

    f = open(file_path, mode="wb")
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("上传成功：%s" % filename)


class UpForm(BootstrapForm):
    """普通 Form 上传：文件由视图自己写盘，数据库自己存路径。"""
    # 文件框不能套 form-control，否则样式错乱
    bootstrap_exclude_fields = ["img"]

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    """普通 Form 上传（配合 Boss 表）"""
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        image_object = form.cleaned_data.get("img")
        filename = os.path.basename(image_object.name)

        # 文件写到 media/boss/，与数据库中保存的相对路径保持一致
        boss_dir = os.path.join(settings.MEDIA_ROOT, "boss")
        if not os.path.exists(boss_dir):
            os.makedirs(boss_dir)

        media_path = os.path.join(boss_dir, filename)
        with open(media_path, mode='wb') as f:
            for chunk in image_object.chunks():
                f.write(chunk)

        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img="boss/" + filename,
        )
        return HttpResponse("上传成功")
    return render(request, "upload_form.html", {"form": form, "title": title})


class UpModelForm(BootstrapModelForm):
    """ModelForm 上传：FileField 自动存到 MEDIA_ROOT/upload_to。"""
    bootstrap_exclude_fields = ["img"]

    class Meta:
        model = models.City
        fields = "__all__"


def upload_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()      # 文件自动保存到 upload_to 目录，路径写入数据库
        return HttpResponse("成功")
    return render(request, 'upload_form.html', {"form": form, 'title': title})


class XXModelForm(BootstrapModelForm):
    """头像预览表单：image 用 FileField，选中文件后在页面内预览。"""
    bootstrap_exclude_fields = ["image"]

    class Meta:
        model = models.XX
        fields = "__all__"


def tt(request):
    """头像预览（tt.html）：上方表单 + 下方已上传头像列表"""
    if request.method == "GET":
        form = XXModelForm()
        queryset = models.XX.objects.all().order_by("-id")
        return render(request, 'tt.html', {"form": form, "queryset": queryset})

    form = XXModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        # 保存后跳回本页，表单清空、列表自动刷新
        return redirect("/tt/")

    queryset = models.XX.objects.all().order_by("-id")
    return render(request, 'tt.html', {"form": form, "queryset": queryset})


def tt_delete(request):
    """删除已上传的头像（同时删掉 media 里的文件）"""
    nid = request.GET.get("nid")
    row_object = models.XX.objects.filter(id=nid).first()
    if row_object:
        row_object.image.delete(save=False)
        row_object.delete()
    return redirect("/tt/")
