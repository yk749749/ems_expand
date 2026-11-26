# app01/views/account.py
"""登录与注销视图。"""
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect, render

from app01 import models
from app01.utils.code import check_code
from app01.utils.encrypt import md5


def login(request):
    """登录"""
    # GET 请求：打开登录页面
    if request.method == "GET":
        return render(request, "login.html")

    # POST 请求：校验用户名、密码和图片验证码
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    code = request.POST.get("code", "").strip()

    # 0. 校验图片验证码
    session_code = request.session.get("image_code", "")
    if not session_code or code.upper() != session_code.upper():
        return render(
            request,
            "login.html",
            {"error": "验证码错误", "username": username},
        )

    # 1. 校验用户名和密码
    admin = models.Admin.objects.filter(
        username=username,
        password=md5(password),
    ).first()

    if not admin:
        return render(
            request,
            "login.html",
            {"error": "用户名或密码错误", "username": username},
        )

    # 2. 登录成功：清除验证码，把当前用户信息写入 session
    request.session.pop("image_code", None)
    request.session["info"] = {"id": admin.id, "name": admin.username}
    return redirect("/admin/list/")


def image_code(request):
    """生成图片验证码，并把验证码字符串保存到 session"""
    img, code_string = check_code()
    request.session["image_code"] = code_string

    stream = BytesIO()
    img.save(stream, format="PNG")

    response = HttpResponse(stream.getvalue(), content_type="image/png")
    # 禁止浏览器缓存，保证每次都能拿到新的验证码
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    return response


def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")
